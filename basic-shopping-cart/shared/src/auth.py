import jwt, os

# get the jwt through the env var
SECRET = os.environ.get('JWT_SECRET', None)
ALGO = os.environ.get('JWT_ENCRYPT', 'HS256')

if not SECRET:
    raise Exception('No JWT secret key, please add one.')

def encode(data):
    return jwt.encode(data, SECRET, algorithm=ALGO)

def decode(jwt):
    return jwt.decode(jwt, SECRET, algorithm=ALGO)

def get_jwt(self, req, resp, resource, params):
    params['jwt'] = decode(req.auth)