from sys import exit

from kubernetes import client, config

try:
    config.load_kube_config()
except FileNotFoundError:
    exit("No '~/.kube/config' found")


def list(action, action_params):
    _common_assertions(action, action_params)

    obj, method_name = _get_k8s_api_object_and_method_name(
        action, action_params)
    method_params = _get_method_params(action_params)

    return getattr(obj, method_name)(*tuple(method_params))


def read(action, action_params):
    pass


def read_or_create(action, action_params):
    pass


def create(action, action_params):
    pass


def create_or_replace(action, action_params):
    pass


def replace(action, action_params):
    pass


def delete(action, action_params):
    pass


def _common_assertions(action, action_params):
    assert 'kind' in action_params, f'kind is a mandatory field for {action}'


def _get_k8s_api_object_and_method_name(action, action_params):
    method = action.split('.')[1]
    kind = action_params['kind']

    # Assemble method name
    method_name = f'{method}_namespaced_{kind}'

    if 'all-namespaces' in action_params:
        method_name = f'{method}_{kind}_for_all_namespaces'

    # Determine the client class to use
    # TODO: take the version from the body instead of doing this crazy loop
    for class_name in dir(client):
        _class = getattr(client, class_name)

        try:
            getattr(_class, method_name)
        except AttributeError:
            continue
        else:
            return_object = _class()

    return return_object, method_name


def _get_method_params(action_params):
    method_params = []

    name = None
    if 'name' in action_params:
        name = action_params['name']
        method_params.append(name)

    namespace = None
    if 'namespace' not in action_params:
        namespace = 'default'
    else:
        namespace = action_params['namespace']

    if 'all-namespaces' not in action_params:
        method_params.append(namespace)

    return method_params
