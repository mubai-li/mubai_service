from enum import Enum,auto


class IntChoicesBaseEnum(Enum):
    def __init__(self, *args, **kwargs):
        self._int_value_ = len(self._member_map_)
        super().__init__()

    @property
    def intvalue(self):
        return self._int_value_
