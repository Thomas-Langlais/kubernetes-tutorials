import logging, traceback, falcon, dotenv
# needs to be done before loading custom components
dotenv.load_dotenv(dotenv.find_dotenv())
import resources.shoppingcart as shoppingcart, util.logging as mylogging, util.api as api

app = falcon.API(middleware=[
    mylogging.LoggingMiddleware('auth-pub.log', 'auth-pub', logging.INFO)
])

app.add_route('/', api.BaseApi())
app.add_route('/api/shopping-cart', shoppingcart.ShoppingCart())