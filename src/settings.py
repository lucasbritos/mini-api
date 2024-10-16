import os

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "DEBUG")
AUTH_REQUEST = os.getenv("AUTH_REQUEST", "True") == "True"
SERVER_DEBUG = os.getenv("SERVER_DEBUG", "True") == "True"
USE_LOCAL_JWKS = os.getenv("USE_LOCAL_JWKS", "False") == "True"
LOCAL_JWKS =  os.getenv("LOCAL_JWKS")
REMOTE_JWKS_ENDPOINT = os.getenv("REMOTE_JWKS_ENDPOINT")