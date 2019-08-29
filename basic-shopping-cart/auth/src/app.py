import logging, traceback, falcon, dotenv
from logging.handlers import RotatingFileHandler

# needs to be done before loading custom components
dotenv.load_dotenv(dotenv.find_dotenv())

import resources.user as user, util.logging as mylogging, util.api as api

app = falcon.API(middleware=[
    mylogging.LoggingMiddleware('auth.log', 'auth', logging.INFO)
])

db_logger = logging.getLogger('auth.db')
db_logger.setLevel(logging.DEBUG)
db_logger.addHandler(RotatingFileHandler('auth.db.log', maxBytes=10000000, backupCount=3))

app.add_route('/', api.BaseApi())
app.add_route('/api/auth/user/{userid}', user.User())