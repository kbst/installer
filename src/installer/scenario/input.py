class Input:

    def __init__(self, input_id, stage_id, input):
        self.id = input_id
        self.stage_id = stage_id

        self.type = input.get('type', 'text')

        assert 'name' in input, 'name is a mandatory field for all inputs'
        self.name = input['name']

        self.value = input.get('value', '')

        self.label = input.get('label', '')

        self.min = input.get('min', None)
        self.max = input.get('max', None)
        self.step = input.get('step', None)

    def __repr__(self):
        return self.name

    def to_dict(self):
        input = {'id': self.id,
                 'stage_id': self.stage_id,
                 'name': self.name,
                 'value': self.value,
                 'label': self.label,
                 'type': self.type,
                 'min': self.min,
                 'max': self.max,
                 'step': self.step}
        return input
