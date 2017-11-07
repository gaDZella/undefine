import re
from FileModel.FragmentType import FragmentType


class ConditionAccessor:
    IfSearchPattern = r"[ \t\f]*#\s*if\s*(.+?)(?:\n|$)"
    ElifSearchPattern = r"[ \t\f]*#\s*elif\s*(.+?)(?:\n|$)"

    @staticmethod
    def get(frag):
        cond = None
        if frag.type is FragmentType.IfStatement:
            cond = re.findall(ConditionAccessor.IfSearchPattern, frag.text)[0]
        if frag.type is FragmentType.ElIfStatement:
            cond = re.findall(ConditionAccessor.ElifSearchPattern, frag.text)[0]
        return cond

    @staticmethod
    def set(frag, value):
        pattern = ""
        fmt = ""
        if frag.type is FragmentType.IfStatement:
            pattern = ConditionAccessor.IfSearchPattern
            fmt = "#if {0}\n"
        if frag.type is FragmentType.ElIfStatement:
            pattern = ConditionAccessor.ElifSearchPattern
            fmt = "#elif {0}\n"
        ConditionAccessor._set(frag, value, pattern, fmt)

    @staticmethod
    def _set(frag, value, pattern, fmt):
        if frag.text is not None:
            res = re.findall(pattern, frag.text)
            if len(res) > 0:
                frag.text = frag.text.replace(res[0], str(value))
                return
        frag.text = str.format(fmt, value)



