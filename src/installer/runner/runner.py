class Runner:

    def __init__(self, scenario):
        self.scenario = scenario
        self.state = RunnerState()

    def run(self):
        for stage in self.scenario.stages:
            for step in stage.steps:
                _result = step.execute(variables=self.state.all())

                if step.register:
                    self.state.set(step.register, _result)


class RunnerState:

    def __init__(self):
        self._variables = dict()

    def all(self):
        return self._variables

    def get(self, key):
        return self._variables[key]

    def set(self, key, value):
        self._variables[key] = value
