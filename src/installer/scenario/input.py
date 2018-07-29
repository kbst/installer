class Input:

    def __init__(self, input_id, stage_id, input):
        self.id = input_id
        self.stage_id = stage_id
        assert 'name' in input, 'name is a mandatory field for all inputs'
        self.name = input['name']

        self.value = input['value']

    def __repr__(self):
        return self.name

    def to_dict(self):
        input = {'id': self.id,
                 'stage_id': self.stage_id,
                 'name': self.name,
                 'value': self.value}
        return input
