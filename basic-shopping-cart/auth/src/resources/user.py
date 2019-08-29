from json import dumps
import psycopg2, logging, falcon

logger = logging.getLogger('auth.db')

CONN_OPTIONS = {'host':'auth-db', 'dbname':'authentication', 'user':'postgres'}

class User(object):
    def on_get(self, req, resp, userid):
        if userid:
            self._get(req, resp, userid)
        else:
            self._get_all(req, resp)
    def on_post(self, req, resp):
        username = req.params.get('username', None)
        email = req.params.get('email', None)
        password = req.params.get('password', None)

        columns = {'id', 'username', 'email'}
        with psycopg2.connect(**CONN_OPTIONS) as conn:
            with conn.cursor() as cur:
                logger.info('inserting user with username=%s and email=%s', username, email)
                cur.execute('INSERT INTO user_account(username, email, password) VALUES(%s,%s,%s) returning id', (username, email, password))
                user_id = cur.fetchone()[0]
                logger.info('inserted user with id %s', user_id)
                user = { key: val for key, val in zip(columns, {user_id, username, email})}
        conn.close()

        resp.status = falcon.HTTP_200
        resp.body = dumps(user)
        resp.set_header('Content-Type', 'application/json')
    
    def _get_all(self, req, resp):
        userid = req.params.get('id', None)
        username = req.params.get('username', None)
        email = req.params.get('email', None)
        whereClause = dict()
        
        if userid: whereClause['id'] = userid
        if username: whereClause['username'] = username
        if email: whereClause['email'] = email
        filterdb = userid != None or username != None or email != None
        
        columns = ['id', 'username', 'email']
        with psycopg2.connect(**CONN_OPTIONS) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT %s FROM user_account' + (' WHERE' + ''.join(map(lambda k: ' AND ' + k + '=%s', whereClause.keys())) if filterdb else ''),
                    (','.join(columns), *whereClause.values())
                )
                
                users = list(map(
                    lambda tup: { key: val for key, val in zip(columns, tup)}, cur.fetchall()
                ))
        conn.close()

        resp.status = falcon.HTTP_200
        resp.body = dumps(users)
        resp.set_header('Content-Type', 'application/json')

    def _get(self, req, resp, userid):
        columns = ['id', 'username', 'email', 'password']
    
        user = None
        with psycopg2.connect(**CONN_OPTIONS) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT %s FROM user_account WHERE id=%s', (','.join(columns), userid))
                user = cur.fetchone()
        conn.close()
        
        if not user:
            resp.status = falcon.HTTP_404
            resp.body = dumps({'message': 'no user found'})
            resp.set_header('Content-Type', 'application/json')
            return

        
        resp.status = falcon.HTTP_200
        resp.body = dumps({ key: val for key, val in zip(columns, user)})
        resp.set_header('Content-Type', 'application/json')