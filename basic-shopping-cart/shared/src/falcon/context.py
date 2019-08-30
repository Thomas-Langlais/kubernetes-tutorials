import logging
try:
    import os, redis
    from json import dumps as json

    REDIS_HOST = os.environ.get('REDIS_HOST', None)
    SESSION_NAME_PREFIX = os.environ('REDIS_SESSION_NAME_PREFIX', 'session:')

    if not REDIS_HOST:
        raise Exception('No host available')

    class FalconContext(object):
        def __init__(self):
            self._redis = redis.Redis(host=REDIS_HOST, db=0, socket_connect_timeout=2, socket_timeout=2)
            self.session = dict()
        
        def get_session(self, userid):
            self.session = json(self._redis.get(SESSION_NAME_PREFIX + userid))
except ImportError as err:
    logging.getLogger().warning('Wont work, redis was not installed')