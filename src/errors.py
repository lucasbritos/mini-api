import settings
import logging
import traceback
from bottle import response

logger = logging.getLogger(__name__)

class AuthorizationError(Exception):
    """Raised when ..."""
    pass

class CustomValidationError(Exception):
    """Raised when ..."""
    pass

def error_handler(exception):
    error_dict = {
        "messsage": str(exception)
    }
    if isinstance(exception, CustomValidationError):
        logger.exception("An error occurred during validation")
        response.status = 400
        error_dict["text"] = "Bad request"
    elif isinstance(exception, AuthorizationError):
        logger.exception("An error occurred during authorization")
        response.status = 401
        error_dict["text"] = "Unauthorized"
    else:
        response.status = 500
        logger.exception("An error occurred during request processing")
        error_dict["text"] = "Server error"
    

    if settings.SERVER_DEBUG:
        error_dict["trace"] = traceback.format_exception(type(exception), exception, exception.__traceback__)

    response.content_type = 'application/json'
    return error_dict