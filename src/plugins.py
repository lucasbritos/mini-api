import time
from bottle import response, request
from errors import error_handler
from auth import validate_header
import settings

def error_handler_plugin(callback):
    def wrapper(*args, **kwargs):
        try:
            response = callback(*args, **kwargs)
            return response
        except Exception as error:
            return error_handler(error)
    return wrapper


def authorize(callback):
    def wrapper(*args, **kwargs):
        if settings.AUTH_REQUEST:
            auth_header = request.headers.get('Authorization')
            username_auth = validate_header(auth_header)
        
        return callback(*args, **kwargs)
    return wrapper

def stopwatch(callback):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = callback(*args, **kwargs)
        end = time.time()
        response.headers['X-Exec-Time'] = str(end - start)
        return result
    return wrapper
