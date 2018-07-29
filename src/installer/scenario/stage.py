from .input import Input
from .step import Step
from .status import Status


class Stage:

    def __init__(self, stage_id, stage):
        self.id = stage_id
        self.status = Status.PENDING

        assert 'name' in stage
        self.name = stage['name']

        assert 'description' in stage
        self.description = stage['description']

        self.inputs = []
        for input_id, input in enumerate(stage['inputs']):
            i = Input(input_id, stage_id, input)
            self.inputs.append(i)

        assert 'steps' in stage
        self.steps = []

        for step_id, step in enumerate(stage['steps']):
            s = Step(step_id, stage_id, step)
            self.steps.append(s)

    def __repr__(self):
        return self.name

    def to_dict(self):
        stage = {}
        stage['id'] = self.id
        stage['name'] = self.name
        stage['description'] = self.description
        stage['inputs'] = []
        stage['steps'] = []
        stage['status'] = {'code': self.status.value,
                           'name': self.status.name}

        for input in self.inputs:
            stage['inputs'].append(input.to_dict())

        for step in self.steps:
            stage['steps'].append(step.to_dict())

        return stage
