import psycopg2, requests

# shoppingcart = Blueprint('shoppingcart', __name__)
CONN_OPTIONS = {'host':'api-db', 'dbname':'shopping-cart', 'user':'postgres'}

class ShoppingCart(object):
    def on_get(self):
        # user = session.get('user', None)
        # if not user:
        #     return ({'error': 'not authorized'}, 401, {'Content-Type': 'application/json'})
        
        with psycopg2.connect(**CONN_OPTIONS) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT i.name,i.price,si.quantity FROM item as i, shopping_cart_item as si, shopping_cart as s WHERE s.id =%s', user['id'])
        conn.close()

        cart = []
        for row in cur:
            cart.append({ key: val for key, val in zip(['name', 'price', 'quantity'], row)})
        
        return cart