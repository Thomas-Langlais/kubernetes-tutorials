from myflask import MyFlask as ApiFlask
from flask.ext.session import Session
from redis import Redis
import shoppingcart

SESSION_TYPE = 'redis'
SESSION_REDIS = Redis(host='redis')
SESSION_COOKIE_NAME = 'sess'
SESSION_KEY_PREFIX = 'session:'

app = ApiFlask(__name__, static_folder=None)
Session(app)

app.register_blueprint(shoppingcart.shoppingcart, url_prefix='/api/shopping-cart')

if __name__ == "__main__":
    print('Spinning up server')
    print(app.url_map)
    app.run(host='0.0.0.0', port='80')