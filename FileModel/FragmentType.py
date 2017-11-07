from enum import Enum, auto


class FragmentType(Enum):
    Body = auto()
    IfStatement = auto()
    ElIfStatement = auto()
    ElseStatement = auto()
    EndIfStatement = auto()
