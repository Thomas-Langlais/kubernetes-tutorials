from flask import Blueprint, request, make_response, session, jsonify
import psycopg2, atexit, requests

service = Blueprint('service', 'service')
connection = psycopg2.connect(host='auth-db', dbname='authentication', user='postgres')
    
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

    columns = ['id', 'username', 'email', 'password']
    cur = connection.cursor()
    cur.execute('SELECT {columns} FROM user WHERE {type}={value}'.format(columns=','.join(columns), **login))
    user = { key: val for key, val in zip(columns, cur.fetchone())}
    session['user'] = user
    cur.close()

    if user == None: return ('', 404)
    if user['password'] != password: return ('', 401)
    
    return jsonify(user)

@service.route('/logout')
def logout():
    # check if it exists in the cache
    if session.get('user', None):
        session.clear()
        return (dict(), 200)
    # doesn't exist, it's ok but return a 201
    return (dict(), 201, {'Content-Type': 'application/json'})

@service.route('/create')
def create():
    username = request.args.get('username', None)
    email = request.args.get('email', None)
    password = request.args.get('password', None)

    if not (username != None and email != None and password != None):
        return ({'message': 'need username, email, and a password'}, 400, {'Content-Type': 'application/json'})

    r = requests.post('auth/api/authentication/user', params={'username': username, 'email': email, 'password': password})
    return r.status_code

atexit.register(lambda: connection.close())