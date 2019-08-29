import services, logging, traceback
from config import Config
from time import strftime
from logging.handlers import RotatingFileHandler
from redis import Redis

app = ApiFlask(__name__, static_folder=None)
app.config.from_object(Config())
Session(app)

app.register_blueprint(services.service, url_prefix='/api/auth')

handler = RotatingFileHandler('auth-pub.log', maxBytes=10000000, backupCount=3)
logger = logging.getLogger('auth-pub')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

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
    return (tb, 500)

@app.route('/', methods=['GET'])
def healthcheck():
    return ('', 200)