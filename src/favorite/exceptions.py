class FavoriteAlreadyExists(Exception):
    def __init__(self, message="Product already exists in favorites."):
        self.message = message
        super().__init__(self.message)


class FavoriteNotFound(Exception):
    def __init__(self, message="Product not found in favorites."):
        self.message = message
        super().__init__(self.message)
