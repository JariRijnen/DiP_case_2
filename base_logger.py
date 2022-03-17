import logging

logger = logging
logger.basicConfig(level=logging.INFO, format=('%(asctime)s %(filename)s[line:%(lineno)d] '
                                               '%(levelname)s%(message)s'),
                   datefmt='%a, %d %b %Y %H:%M:%S', filename='logs/log.log', filemode='w')
