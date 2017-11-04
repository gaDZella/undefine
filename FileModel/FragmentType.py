from enum import Enum


class FragmentType(Enum):
    Body = 0
    IfStatement = 1
    ElIfStatement = 2
    ElseStatement = 3
    EndIfStatement = 4
