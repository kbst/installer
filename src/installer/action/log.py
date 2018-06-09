import logging


def info(action, params):
    assert 'msg' in params, 'msg field required for log.info'
    logging.info(params['msg'])
    return None


def warn(action, params):
    assert 'msg' in params, 'msg field required for log.warn'
    logging.warn(params['msg'])
    return None


def debug(action, params):
    assert 'msg' in params, 'msg field required for log.debug'
    logging.debug(params['msg'])
    return None
