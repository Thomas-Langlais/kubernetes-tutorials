class BaseApi(object):
    def on_get(self, req, res):
        res.status = 200
        res.body = ''