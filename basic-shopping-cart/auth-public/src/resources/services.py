import logging, requests, falcon, shared
from json import dumps as json

AUTH = lambda s: 'http://auth' + s

logger.logging.getLogger('auth-pub')

@falcon.before(shared.auth.get_jwt)
@falcon.before(shared.redis.get_session)
class AuthenticationLogin(object):
    def on_get(self, req, resp, jwt, session):
        # check if it exists in the cache
        user = session.get('user', None)
        if not user:
            resp.status = falcon.HTTP_200
            resp.body = json(user)
            resp.set_header('Content-Type', 'application/json')
            return

        username = req.params.get('username', None)
        email = req.params.get('email', None)
        password = req.params.get('password', None)

        login = {
            'type': 'username',
            'value': username
        }
        if login['value'] == None:
            login.update({
                'type': 'email',
                'value': email
            })
        
        if login['value'] == None:
            resp.status = falcon.HTTP_400
            resp.body = json({
                'error': 'either the email of username needs to be given'
            })
            resp.set_header('Content-Type'. 'application/json')
            return
        
        get_resp = requests.get(AUTH('/api/auth/user'), {login['type']: login['value']})
        users = get_resp.json()
        
        if len(users) > 1:
            resp.status = falcon.HTTP_400
            resp.body = json({'message': 'there should only be 1 user with that thing'})
            resp.set_header('Content-Type', 'application/json')
            return
        
        user = users[0]
        if user['password'] != password:
            resp.status = falcon.HTTP_401
            resp.body = json({})
            resp.set_header('Content-Type', 'application/json')
            return
        
        session['user'] = user
        
        return jsonify(user)

class AuthenticationLogout(object):
    def on_get(self, req, resp, jwt, session):
        # check if it exists in the cache
        if session.get('user', None):
            session.clear()
            resp.status = falcon.HTTP_204
            return
        # doesn't exist, it's ok but return a 201
        resp.status = falcon.HTTP_200

class AuthenticationCreate(object):
    def on_post(self, req, resp, jwt, session):
        username = req.params.get('username', None)
        email = req.params.get('email', None)
        password = req.params.get('password', None)

        if not (username != None and email != None and password != None):
            resp.status = falcon.HTTP_400
            resp.body = json({'message': 'need username, email, and a password'})
            resp.set_header('Content-Type', 'application/json')
            return

        r = requests.post(AUTH('/api/auth/user'), params={'username': username, 'email': email, 'password': password})
        logger.info(r)
        
        session['user'] = r.json()
        resp.status = falcon.HTTP_204
        return