import logging
import logging.config
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.DEBUG)

normalFormatter = logging.Formatter('%(asctime)s loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() L-%(lineno)-4d %(message)s\n')
consoleHandler.setFormatter(normalFormatter)

detailedConsoleHandler = logging.StreamHandler(sys.stdout)
detailedConsoleHandler.setLevel(logging.DEBUG)

detailedFormatter = logging.Formatter('%(asctime)s loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() L-%(lineno)-4d %(message)s   call_trace=%(pathname)s L%(lineno)-4d')
detailedConsoleHandler.setFormatter(detailedFormatter)

logger.addHandler(consoleHandler)

nutrimatch_logger = logging.getLogger('nutrimatch')
nutrimatch_logger.setLevel(logging.DEBUG)
nutrimatch_logger.propagate = False
nutrimatch_logger.addHandler(detailedConsoleHandler)