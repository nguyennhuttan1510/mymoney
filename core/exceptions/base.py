class BusinessException(Exception):
    """
    Base class cho mọi business exception trong hệ thống.
    """
    error_code = "BUSINESS_ERROR"
    message = "An unknown business error occurred."
    status_code = 400

    def __init__(self, message: str | None = None, error_code: str | None = None, payload=None):
        super().__init__(message or self.message)
        self.message = message or self.message
        self.error_code = error_code or self.error_code
        self.payload = payload or {}