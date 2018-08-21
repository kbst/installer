import logging
import json

import tornado.ioloop
import tornado.web
import tornado.websocket
from jsonrpc import JSONRPCResponseManager, dispatcher
from jsonrpc.utils import DatetimeDecimalEncoder


logger = logging.getLogger(__name__)


def response_serialize(obj):
    return json.dumps(obj, cls=DatetimeDecimalEncoder)


class WebsocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        logger.info("websocket opened")

    def on_message(self, message):
        response = JSONRPCResponseManager.handle(message, dispatcher)

        if response.error:
            logger.error(response.error)

        response.serialize = response_serialize
        self.write_message(response.json)

    def on_close(self):
        logger.info("websocket closed")


def application():
    return tornado.web.Application([
        (r"/jsonrpc", WebsocketHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {
            "path": "ui/",
            "default_filename": "index.html"})
    ])


def serve(port=4100):
    app = application()
    app.listen(port)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()
        exit()
