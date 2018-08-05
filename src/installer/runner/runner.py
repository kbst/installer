import logging

from jsonrpc import dispatcher

from scenario.status import Status


logger = logging.getLogger(__name__)


class Runner:
    """
    Here be dragons, Runner is a singleton
    """

    def __new__(cls):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)
            cls.instance._scenario = dict()
            cls.instance._inputs = dict()
            cls.instance._variables = dict()
        return cls.instance

    @property
    def scenario(self):
        return self._scenario

    @scenario.setter
    def scenario(self, scenario):
        self._scenario = scenario

        # Register inputs
        for stage in self.scenario.stages:
            for input in stage.inputs:
                self.register_input(input.name, input.stage_id, input.id)

    def get_stage(self, id):
        return self.scenario.stages[id]

    @property
    def inputs(self):
        return_inputs = {}
        for name in self._inputs:
            stage_id, input_id = self._inputs[name]
            input = self.get_stage(stage_id).inputs[input_id]
            return_inputs[name] = input.value
        return return_inputs

    def register_input(self, name, stage_id, input_id):
        self._inputs[name] = (stage_id, input_id)

    @property
    def variables(self):
        return_vars = {}
        for name in self._variables:
            stage_id, step_id = self._variables[name]
            step = self.get_stage(stage_id).steps[step_id]
            return_vars[name] = step.result
        return return_vars

    def register_var(self, name, stage_id, step_id):
        self._variables[name] = (stage_id, step_id)


@dispatcher.add_method
def get_scenario(**kwargs):
    logger.info("get_scenario method called")
    return Runner().scenario.to_dict()


@dispatcher.add_method
def run(**kwargs):
    logger.info("run method called")
    r = Runner()
    for stage in r.scenario.stages:
        if stage.status == Status.SUCCESS:
            continue

        for step in stage.steps:
            if step.status == Status.SUCCESS:
                continue

            try:
                result = step.execute(inputs=r.inputs,
                                      variables=r.variables)
            except Exception as e:
                # Mark scenario and stage as errors
                r.scenario.status = Status.ERROR
                stage.status = Status.ERROR
                logger.exception(e)
                raise e

            step.result = result
            if step.register:
                r.register_var(step.register, step.stage_id, step.id)

            return r.scenario.to_dict()

        # Stage completed successfully
        stage.status = Status.SUCCESS

        return r.scenario.to_dict()

    # Sceneario completed successfully
    r.scenario.status = Status.SUCCESS

    return r.scenario.to_dict()


@dispatcher.add_method
def update_inputs(payload, **kwargs):
    logger.info("update_inputs method called")
    r = Runner()
    r.scenario.update_inputs(payload)
    return r.scenario.to_dict()
