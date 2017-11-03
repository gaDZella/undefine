from enum import Enum


class FragmentType(Enum):
    Unknown = 0,
    Body = 1
    IfStatement = 2
    ElIfStatement = 3
    ElseStatement = 4
    EndIfStatement = 5
