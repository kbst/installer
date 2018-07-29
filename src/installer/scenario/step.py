from importlib import import_module

import yaml
from jinja2 import Template

from .status import Status


class Step:

    def __init__(self, step_id, stage_id, step):
        self.id = step_id
        self.stage_id = stage_id
        self.status = Status.PENDING
        assert 'name' in step, 'name is a mandatory field for all steps'
        self.name = step['name']
        self.result = None

        self.raw_action = None
        self.method = None
        self.params = None
        for action in step:
            if action in ['name', 'register']:
                continue

            self.raw_action = yaml.dump({action: step[action]})

            assert len(action.split('.')) is 2, \
                f"{action} is not in valid format 'type.action'"
            pkg_name, method_name = action.split('.')

            pkg = import_module(f'action.{pkg_name}')
            self.method = getattr(pkg, method_name)
            self.params = (action, step[action])

        self.register = None
        if 'register' in step:
            self.register = step['register']

    def execute(self, variables=None):
        if self.status is not Status.PENDING:
            return None

        action = self.params[0]
        step_input = self.params[1]

        rendered_input = dict()
        for key in step_input:
            value = step_input[key]
            try:
                template = Template(value)
            except TypeError:
                rendered_input[key] = value
            else:
                rendered_input[key] = template.render(**variables)

        try:
            result = self.method(action, rendered_input)
        except Exception as e:
            self.status = Status.ERROR
            raise e
        else:
            self.status = Status.SUCCESS
            return result

    def __repr__(self):
        return self.name

    def to_dict(self):
        step = {'id': self.id,
                'stage_id': self.stage_id,
                'name': self.name,
                'result': self.result,
                'status': {'code': self.status.value,
                           'name': self.status.name}}
        return step
