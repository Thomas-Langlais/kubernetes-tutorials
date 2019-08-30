import os, logging

try:
    import jwt

    # get the jwt through the env var
    SECRET = os.environ.get('JWT_SECRET', None)
    ALGO = os.environ.get('JWT_ENCRYPT', 'HS256')

    if not SECRET:
        raise Exception('No JWT secret key, please add one.')

    def encode(data):
        return jwt.encode(data, SECRET, algorithm=ALGO)

    def decode(jwt_obj):
        return jwt.decode(jwt_obj, SECRET, algorithm=ALGO)

    def get_jwt(self, req, resp, resource, params):
        params['jwt'] = decode(req.auth)
except ImportError as err:
    logging.getLogger().warning('PyJWT is not installed, this module will not work')