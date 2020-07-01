import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger('cribbage')
logger.setLevel(logging.INFO)

def setLogLevel(on):
    if on:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARN)
