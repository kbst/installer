from importlib import import_module

from jinja2 import Template


class Step:

    def __init__(self, step):
        assert 'name' in step, 'name is a mandatory field for all steps'
        self.name = step['name']

        self.register = None
        if 'register' in step:
            self.register = step['register']

        self.method = None
        self.params = None
        for action in step:
            if action in ['name', 'register']:
                continue

            assert len(action.split('.')) is 2, \
                f"{action} is not in valid format 'type.action'"
            pkg_name, method_name = action.split('.')

            pkg = import_module(f'action.{pkg_name}')
            self.method = getattr(pkg, method_name)
            self.params = (action, step[action])

    def execute(self, variables=None):
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

        return self.method(action, rendered_input)

    def __repr__(self):
        return self.name
