class Runner:
    scenario = None
    state = None

    def __init__(self, scenario):
        self.scenario = scenario
        self.state = RunnerState()

    def run(self):
        for event in self.scenario.events:
            for step in event.steps:
                _result = step.execute(variables=self.state.all())

                if step.register:
                    self.state.set(step.register, _result)


class RunnerState:
    _variables = dict()

    def all(self):
        return self._variables

    def get(self, key):
        return self._variables[key]

    def set(self, key, value):
        self._variables[key] = value
