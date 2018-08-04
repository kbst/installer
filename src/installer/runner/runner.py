import logging
import json

import tornado.ioloop
import tornado.web
import tornado.websocket
from jsonrpc import JSONRPCResponseManager, dispatcher
from jsonrpc.utils import DatetimeDecimalEncoder

from scenario.status import Status
from scenario.input import Input


class Runner:
    """
    Here be dragons, Runner is a singleton
    """

    def __new__(cls):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)
            cls._scenario = None
            cls.instance.inputs = dict()
            cls.instance.variables = dict()
        return cls.instance

    @property
    def scenario(self):
        return self._scenario

    @scenario.setter
    def scenario(self, scenario):
        self._scenario = scenario

    def get_all_inputs(self):
        return_inputs = {}
        for name in self.inputs:
            stage_id, input_id = self.inputs[name]
            input = self.scenario.stages[stage_id].inputs[input_id]
            return_inputs[name] = input.value
        return return_inputs

    def get_input(self, name):
        stage_id, input_id = self.inputs[name]
        input = self.scenario.stages[stage_id].inputs[input_id]
        return input.value

    def set_input(self, name, stage_id, input_id):
        self.inputs[name] = (stage_id, input_id)

    def get_all_vars(self):
        return_vars = {}
        for name in self.variables:
            stage_id, step_id = self.variables[name]
            step = self.scenario.stages[stage_id].steps[step_id]
            return_vars[name] = step.result
        return return_vars

    def get_var(self, name):
        stage_id, step_id = self.variables[name]
        step = self.scenario.stages[stage_id].steps[step_id]
        return step.result

    def set_var(self, name, stage_id, step_id):
        self.variables[name] = (stage_id, step_id)


@dispatcher.add_method
def get_scenario(**kwargs):
    logging.info("get_scenario method called")
    return Runner().scenario.to_dict()


@dispatcher.add_method
def run(**kwargs):
    logging.info("run method called")
    r = Runner()
    for stage in r.scenario.stages:
        if stage.status == Status.SUCCESS:
            continue

        for input in stage.inputs:
            r.set_input(input.name, input.stage_id, input.id)

        for step in stage.steps:
            if step.status == Status.SUCCESS:
                continue

            try:
                result = step.execute(inputs=r.get_all_inputs(),
                                      variables=r.get_all_vars())
            except Exception as e:
                # Mark scenario and stage as errors
                r.scenario.status = Status.ERROR
                stage.status = Status.ERROR
                logging.exception(e)
                raise e

            step.result = result
            if step.register:
                r.set_var(step.register, step.stage_id, step.id)

            return r.scenario.to_dict()

        # Stage completed successfully
        stage.status = Status.SUCCESS

        return r.scenario.to_dict()

    # Sceneario completed successfully
    r.scenario.status = Status.SUCCESS

    return r.scenario.to_dict()


@dispatcher.add_method
def update_inputs(scenario, **kwargs):
    logging.info("update_inputs method called")
    r = Runner()

    for stage in scenario['stages']:
        s = r.scenario.stages[stage['id']]
        for input in stage['inputs']:
            i = Input(input['id'], input['stage_id'], input)
            s.inputs[i.id] = i
            r.set_input(i.name, i.stage_id, i.id)

    return r.scenario.to_dict()


def response_serialize(obj):
    return json.dumps(obj, cls=DatetimeDecimalEncoder)


class WebsocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("WebSocket opened")

    def on_message(self, message):
        response = JSONRPCResponseManager.handle(message, dispatcher)

        if response.error:
            logging.error(response.error)

        response.serialize = response_serialize
        self.write_message(response.json)

    def on_close(self):
        logging.info("WebSocket closed")


def application():
    return tornado.web.Application([
        (r"/jsonrpc", WebsocketHandler),
    ])


def serve(port=4100):
    app = application()
    app.listen(port)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()
        exit()
