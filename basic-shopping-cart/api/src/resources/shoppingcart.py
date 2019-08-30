import psycopg2, requests, falcon, json
import shared

CONN_OPTIONS = {'host':'api-db', 'dbname':'shopping-cart', 'user':'postgres'}

@falcon.before(shared.auth.get_jwt)
@falcon.before(shared.redis.get_session)
class ShoppingCart(object):
    def on_get(self, req, resp, jwt, session):
        user = session.get('user', None)
        if not user:
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({'error': 'not authorized'})
            resp.set_header('Content-Type', 'application/json')
            return
        
        with psycopg2.connect(**CONN_OPTIONS) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT i.name,i.price,si.quantity FROM item as i, shopping_cart_item as si, shopping_cart as s WHERE s.id =%s', user['id'])
        conn.close()

        cart = []
        for row in cur:
            cart.append({ key: val for key, val in zip(['name', 'price', 'quantity'], row)})
        
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(cart)
        resp.set_header('Content-Type', 'application/json')