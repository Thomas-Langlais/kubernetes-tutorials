import services, logging, traceback
from myflask import MyFlask as ApiFlask
from flask import request
from time import strftime
from logging.handlers import RotatingFileHandler
from flask_session import Session
from redis import Redis

SESSION_TYPE = 'redis'
SESSION_REDIS = Redis(host='redis')
SESSION_COOKIE_NAME = 'sess'
SESSION_KEY_PREFIX = 'session:'

app = ApiFlask(__name__, static_folder=None)
Session(app)

app.register_blueprint(services.service, url_prefix='/api/auth')

@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logger.info('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response

@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
    return e.status_code

if __name__ == "__main__":
    handler = RotatingFileHandler('auth-pub.log', maxBytes=10000000, backupCount=3)
    logger = logging.getLogger('auth-pub')
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    logger.info('Spinning up server')
    app.run(host='0.0.0.0', port='80')