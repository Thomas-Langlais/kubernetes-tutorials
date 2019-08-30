import os, logging, json, uuid
try:
    from redis import Redis

    HOST = os.environ.get('REDIS_HOST', None)
    SESSION_NAME_PREFIX = os.environ('REDIS_SESSION_NAME_PREFIX', 'session:')

    if not HOST:
        raise Exception('No redis host specific...')

    redis = Redis(host=HOST, db=0, socket_connect_timeout=2, socket_timeout=2)

    def get_session(req, resp, resource, params):
        if 'jwt' not in params:
            params['session'] = None
            return
        
        req.context.get_session(SESSION_NAME_PREFIX + params['jwt']['session_id'])
        params['session'] = req.context.session
        
except ImportError as err:
    logging.getLogger().warning('Redis is not installed, this module work work')
