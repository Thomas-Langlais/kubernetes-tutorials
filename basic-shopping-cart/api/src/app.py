import logging, traceback, falcon, shared
from resources.shoppingcart import ShoppingCart

app = falcon.API(middleware=[
    shared.logging.LoggingMiddleware('auth-pub.log', 'auth-pub', logging.INFO)
], request_type=shared.falcon.Request)

app.add_route('/', shared.api.BaseApi())
app.add_route('/api/shopping-cart', ShoppingCart())