"""
The shared python module that is distributed to many source code directories
"""
import dotenv
# needs to be done before loading custom components
dotenv.load_dotenv(dotenv.find_dotenv())
from . import falcon, auth, redis
from .util import *
