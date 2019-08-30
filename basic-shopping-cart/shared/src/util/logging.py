import logging
from logging.handlers import RotatingFileHandler
from time import strftime

class LoggingMiddleware(object):
    def __init__(self, logfile_name, logger_name, level):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)
        self.logger.addHandler(RotatingFileHandler(logfile_name, maxBytes=10000000, backupCount=3))

    def process_response(self, req, resp):
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        self.logger.info('%s %s %s %s %s %s', timestamp, req.remote_addr, req.method, req.scheme, req.path, resp.status)
    
    # def process_response(self, req, resp, resource, req_succeeded):
    #     pass