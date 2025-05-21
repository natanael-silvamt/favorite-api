from typing import Type


class SingletonMixin:
    __instance = None

    def __new__(cls: Type) -> 'SingletonMixin':
        if cls.__instance is None:
            cls.__instance = super(SingletonMixin, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
