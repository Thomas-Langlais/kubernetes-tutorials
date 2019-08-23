from flask import Blueprint, request, jsonify
import psycopg2, atexit

user = Blueprint('user', 'user')
connection = psycopg2.connect(host='auth-db', dbname='authentication', user='postgres')
    
@user.route('/<userid>')
def get_user(userid):

    columns = ['id', 'username', 'email']
    cur = connection.cursor()
    cur.execute('SELECT %s FROM user WHERE id=%s', (','.join(columns), userid))
    user = cur.fetchone()
    cur.close()
    
    if user == None:
        return dict()
    return jsonify({ key: val for key, val in zip(columns, user)})

@user.route('/', methods=['POST'])
def create_user():
    username = request.args.get('username', None)
    email = request.args.get('email', None)
    password = request.args.get('password', None)

    cur = connection.cursor()
    cur.execute('INSERT INTO user(username, email, password) VALUES(%s,%s,%s)', (username, email, password))
    
    columns = ['id', 'username', 'email']
    cur.execute('SELECT %s FROM user WHERE username=%s AND email=%s', (','.join(columns), username, email))

    return jsonify({ key: val for key, val in zip(columns, user)})

atexit.register(lambda: connection.close())