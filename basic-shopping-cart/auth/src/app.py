from myflask import MyFlask as ApiFlask
import user, logging, traceback
from flask import request
from time import strftime
from logging.handlers import RotatingFileHandler

app = ApiFlask(__name__, static_folder=None)

app.register_blueprint(user.user, url_prefix='/api/auth/user')

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
    handler = RotatingFileHandler('auth.log', maxBytes=10000000, backupCount=3)
    logger = logging.getLogger('auth')
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    logger.info('Spinning up server')
    app.run(host='0.0.0.0', port='80')