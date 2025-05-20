class NotFoundException(ValueError):
    def __init__(self, message: str = "Object not found"):
        super().__init__(message)
        self.message = message


class UniqueViolation(Exception):
    def __init__(self, message: str = "Unique constraint violation"):
        super().__init__(message)
        self.message = message


class RequestError(Exception):
    def __init__(self: 'RequestError', message: str = 'Request Error', status_code: int = 500) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
