class UserNotFound(Exception):
    def __init__(self: 'UserNotFound', message: str = 'User not found') -> None:
        self.message = message
        super().__init__(self.message)


class UserInactive(Exception):
    def __init__(self: 'UserInactive', message: str = 'User inactive') -> None:
        self.message = message
        super().__init__(self.message)


class EmailOrPasswordInvalid(Exception):
    def __init__(self: 'EmailOrPasswordInvalid', message: str = 'Email or password invalid') -> None:
        self.message = message
        super().__init__(self.message)
