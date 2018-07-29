class Input:

    def __init__(self, input_id, input):
        self.id = input_id
        assert 'name' in input, 'name is a mandatory field for all inputs'
        self.name = input['name']

    def __repr__(self):
        return self.name

    def to_dict(self):
        input = {'id': self.id,
                 'name': self.name}
        return input
