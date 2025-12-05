from core.exceptions.base import BusinessException


class SessionException(BusinessException):
    error_code = "SESSION_ERROR"
    message = "Something wrong with session."
    status_code = 401


class SessionInvalid(SessionException):
    error_code = "SESSION_INVALID"
    message = 'Session invalid'
    status_code = 401


class SessionExpired(SessionException):
    error_code = 'SESSION_EXPIRED'
    message = 'Session expired'
    status_code = 401


class SessionInactive(SessionException):
    error_code = "SESSION_INACTIVE"
    message = 'Session inactive'
    status_code = 401
