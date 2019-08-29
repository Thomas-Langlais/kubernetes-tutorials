from flask import Blueprint, request, make_response, session, jsonify
import requests, logging

service = Blueprint('service', 'service')
AUTH = lambda s: 'http://auth' + s

logger = logging.getLogger('auth-pub')

@service.route('/login')
def login():
    # check if it exists in the cache
    user = session.get('user', None)
    if user != None:
        return jsonify(user)

    username = request.args.get('username', None)
    email = request.args.get('email', None)
    password = request.args.get('password', None)

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
        resp = make_response({
            'error': 'either the email of username needs to be given'
        }, 400)
        resp.headers['Content-Type'] = 'application/json'
        return resp
    
    resp = requests.get(AUTH('/api/auth/user'), {login['type']: login['value']})
    users = resp.json()
    
    if len(users) > 1:
        return (jsonify({'message': 'there should only be 1 user with that thing'}), 400)
    
    user = users[0]
    if user['password'] != password: return ('', 401)
    
    session['user'] = user
    
    return jsonify(user)

@service.route('/logout')
def logout():
    # check if it exists in the cache
    if session.get('user', None):
        session.clear()
        return (dict(), 200)
    # doesn't exist, it's ok but return a 201
    return (dict(), 201, {'Content-Type': 'application/json'})

@service.route('/create', methods=['POST'])
def create():
    username = request.args.get('username', None)
    email = request.args.get('email', None)
    password = request.args.get('password', None)

    if not (username != None and email != None and password != None):
        return ({'message': 'need username, email, and a password'}, 400, {'Content-Type': 'application/json'})

    r = requests.post(AUTH('/api/auth/user'), params={'username': username, 'email': email, 'password': password})
    logger.info(r)
    
    session['user'] = r.json()
    return ('', r.status_code)