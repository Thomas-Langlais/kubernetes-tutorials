from redis import Redis

class Config(object):
    SESSION_TYPE = 'redis'
    SESSION_REDIS = Redis(host='redis')
    SESSION_COOKIE_NAME = 'sess'
    SESSION_KEY_PREFIX = 'session:'
    SECRET_KEY = 'api'