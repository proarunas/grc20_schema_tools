from enum import Enum, auto
from typing import NamedTuple


class ErrType(Enum):
    KEY_DUPLICATE = auto()

    ID_MISSING = auto()
    ID_DUPLICATE = auto()
    ID_INVALID = auto()

    TYPE_INVALID = auto()
    PARAM_ORPHANED = auto()
    RELATION_INVALID = auto()

    NAME_MISSING = auto()
    NAME_DUPLICATE = auto()

    VALUE_MISSING = auto()
    VALUE_DUPLICATE = auto()

    UNDEFINED = auto()


class ValErr(NamedTuple):
    error_type: ErrType
    entity_path: list[str]
    message: str

    def print(self):
        return f"{self.error_type} in `{".".join(self.entity_path)}`: {self.message}"
