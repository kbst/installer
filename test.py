#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from sys import exit

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect


class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.connect()
        PeriodicCallback(self.keep_alive, 20000).start()
        self.ioloop.start()

    @gen.coroutine
    def connect(self):
        print("trying to connect")
        try:
            self.ws = yield websocket_connect(self.url)
        except Exception as e:
            print("connection error")
        else:
            print("connected")
            self.run()

    @gen.coroutine
    def run(self):
        while True:
            payload = {
                "method": "run",
                "params": None,
                "jsonrpc": "2.0",
                "id": 0,
            }

            # Send rpc request
            yield self.ws.write_message(json.dumps(payload))

            # Read responses
            msg = yield self.ws.read_message()

            m = json.loads(msg)
            scenario = m['result']

            print('\n\n')
            print('\n\n')
            print('\n\n')
            print('\n\n')
            print(f"Scenario :: {scenario['status']['name']}")
            for stage in scenario['stages']:
                print('\n\n')
                print('\n\n')
                print(f"Stage :: {stage['status']['name']}")
                for step in stage['steps']:
                    print(f"Step :: {step['status']['name']}")

            status_code = scenario['status']['code']
            if status_code > 0:
                exit(status_code)

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message("keep alive")


if __name__ == "__main__":
    client = Client("ws://localhost:4100/jsonrpc", 5)
