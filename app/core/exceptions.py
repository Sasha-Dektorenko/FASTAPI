class BaseAppException(Exception):
    """Base exception class for the application."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(BaseAppException):
    """Exception raised when a requested resource is not found."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)
    
class ValidationException(BaseAppException):
    """Exception raised for validation errors."""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=400)

class ConflictException(BaseAppException):
    """Exception raised for conflict errors, such as duplicate entries."""
    def __init__(self, message: str = "Conflict error"):
        super().__init__(message, status_code=409)