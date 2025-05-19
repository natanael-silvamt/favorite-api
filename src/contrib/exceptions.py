class NotFoundException(ValueError):
    def __init__(self, message: str = "Object not found"):
        super().__init__(message)
        self.message = message


class UniqueViolation(Exception):
    def __init__(self, message: str = "Unique constraint violation"):
        super().__init__(message)
        self.message = message
