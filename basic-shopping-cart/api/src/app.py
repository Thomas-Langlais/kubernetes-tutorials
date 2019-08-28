from config import Config
from redis import Redis
import logging, traceback, falcon
import shoppingcart, util.logging as mylogging, util.api as api

app = falcon.API(middleware=[
    mylogging.LoggingMiddleware('auth-pub.log', 'auth-pub', logging.INFO)
])

app.add_route('/', api.BaseApi())
app.add_route('/api/shopping-cart', shoppingcart.ShoppingCart())