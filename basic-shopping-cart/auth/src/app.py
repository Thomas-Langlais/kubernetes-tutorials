import logging, traceback, falcon, shared
from logging.handlers import RotatingFileHandler
from resources.user import User

app = falcon.API(middleware=[
    shared.logging.LoggingMiddleware('auth.log', 'auth', logging.INFO)
], request_type=shared.falcon.Request)

db_logger = logging.getLogger('auth.db')
db_logger.setLevel(logging.DEBUG)
db_logger.addHandler(RotatingFileHandler('auth.db.log', maxBytes=10000000, backupCount=3))

app.add_route('/', shared.api.BaseApi())
app.add_route('/api/auth/user/{userid}', User())