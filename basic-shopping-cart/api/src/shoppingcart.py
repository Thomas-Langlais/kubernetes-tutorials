from flask import Blueprint, session
import psycopg2, requests, atexit

shoppingcart = Blueprint('shoppingcart', __name__)
connection = psycopg2.connect(host='api-db', dbname='shopping-cart', user='postgres')
    
@shoppingcart.route('/')
def get_cart():
    user = session.get('user', None)
    if not user:
        return ({'error': 'not authorized'}, 401, {'Content-Type': 'application/json'})
    
    print('authorized to look at cart')
    cur = connection.cursor()
    cur.execute('SELECT i.name,i.price,si.quantity FROM item as i, shopping_cart_item as si, shopping_cart as s WHERE s.id =%s', user['id'])

    cart = []
    for row in cur:
        cart.append({ key: val for key, val in zip(['name', 'price', 'quantity'], row)})
    
    return cart

atexit.register(lambda: connection.close())