import traceback, falcon, logging, shared
from resources.services import AuthenticationCreate, AuthenticationLogin, AuthenticationLogout

app = falcon.API(middleware=[
    shared.logging.LoggingMiddleware('auth-pub.log', 'auth-pub', logging.INFO)
], request_type=shared.falcon.Request)

app.add_route('/', shared.api.BaseApi())
app.add_route('/api/auth/create', AuthenticationCreate())
app.add_route('/api/auth/login', AuthenticationLogin())
app.add_route('/api/auth/logout', AuthenticationLogout())