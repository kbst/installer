import logging


logger = logging.getLogger(__name__)


def info(action, params):
    assert 'msg' in params, 'msg field required for log.info'
    message = params['msg']
    logger.info(message)
    return message


def warn(action, params):
    assert 'msg' in params, 'msg field required for log.warn'
    message = params['msg']
    logger.info(message)
    return message


def debug(action, params):
    assert 'msg' in params, 'msg field required for log.debug'
    message = params['msg']
    logger.info(message)
    return message
