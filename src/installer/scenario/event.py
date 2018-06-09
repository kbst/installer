from .step import Step


class Event:
    steps = []

    def __init__(self, event):
        assert 'name' in event
        assert 'steps' in event

        for step in event['steps']:
            s = Step(step)
            self.steps.append(s)
