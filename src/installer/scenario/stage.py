from .step import Step


class Stage:

    def __init__(self, stage):
        assert 'name' in stage
        self.name = stage['name']

        assert 'description' in stage
        self.description = stage['description']

        assert 'steps' in stage
        self.steps = []

        for step in stage['steps']:
            s = Step(step)
            self.steps.append(s)

    def __repr__(self):
        return self.name
