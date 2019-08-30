import falcon
from .context import FalconContext

class Request(falcon.Request):
    context_type = FalconContext