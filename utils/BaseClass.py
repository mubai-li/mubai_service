from enum import Enum,auto


class IntChoicesBaseEnum(Enum):
    def __init__(self, *args, **kwargs):
        self._int_value_ = len(self._member_map_)
        super().__init__()

    @property
    def intvalue(self):
        return self._int_value_


class AbstractSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None or cls._instance.__class__.__name__ != cls.__name__:
            orig = super(cls.__mro__[-2], cls)
            cls._instance = orig.__new__(cls)
        return cls._instance



