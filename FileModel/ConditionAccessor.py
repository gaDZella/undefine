import re
from FileModel.FragmentType import FragmentType


IfSearchPattern = r"[ \t\f]*#\s*if\s*(.+?)(?:\n|$)"
ElifSearchPattern = r"[ \t\f]*#\s*elif\s*(.+?)(?:\n|$)"


def get_condition(frag):
    cond = None
    if frag.type is FragmentType.IfStatement:
        cond = re.findall(IfSearchPattern, frag.text)[0]
    if frag.type is FragmentType.ElIfStatement:
        cond = re.findall(ElifSearchPattern, frag.text)[0]
    return cond


def set_condition(frag, value):
    pattern = ""
    fmt = None
    if frag.type is FragmentType.IfStatement:
        pattern = IfSearchPattern
        fmt = "#if {0}\n"
    if frag.type is FragmentType.ElIfStatement:
        pattern = ElifSearchPattern
        fmt = "#elif {0}\n"
    _set(frag, value, pattern, fmt)


def _set(frag, value, pattern, fmt):
    if fmt is not None:
        if frag.text is not None:
            res = re.findall(pattern, frag.text)
            if len(res) > 0:
                frag.text = frag.text.replace(res[0], str(value))
                return
        frag.text = str.format(fmt, value)



