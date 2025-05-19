class ClientNotFound(Exception):
    def __init__(self, message="Client not found."):
        super().__init__(message)
        self.message = message


class DuplicateEmail(Exception):
    def __init__(self, message="Email already exists."):
        super().__init__(message)
        self.message = message
