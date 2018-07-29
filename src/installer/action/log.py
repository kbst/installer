import logging


def info(action, params):
    assert 'msg' in params, 'msg field required for log.info'
    message = params['msg']
    logging.info(message)
    return message


def warn(action, params):
    assert 'msg' in params, 'msg field required for log.warn'
    message = params['msg']
    logging.info(message)
    return message


def debug(action, params):
    assert 'msg' in params, 'msg field required for log.debug'
    message = params['msg']
    logging.info(message)
    return message
