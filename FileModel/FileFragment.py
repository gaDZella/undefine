import re
from FileModel.FragmentType import FragmentType


class FileFragment:
    IfSearchPattern = r"[ \t\f]*#\s*if\s*(.+?)(?:\n|$)"
    ElifSearchPattern = r"[ \t\f]*#\s*elif\s*(.+?)(?:\n|$)"

    def __init__(self, fType, text):
        self.type = fType
        self.text = text

    def get_condition(self):
        cond = None
        if self.type is FragmentType.IfStatement:
            cond = re.findall(FileFragment.IfSearchPattern, self.text)[0]
        if self.type is FragmentType.ElIfStatement:
            cond = re.findall(FileFragment.ElifSearchPattern, self.text)[0]
        return cond

    def set_condition(self, value):
        pattern = ""
        fmt = ""
        if self.type is FragmentType.IfStatement:
            pattern = FileFragment.IfSearchPattern
            fmt = "#if {0}\n"
        if self.type is FragmentType.ElIfStatement:
            pattern = FileFragment.ElifSearchPattern
            fmt = "#elif {0}\n"
        self._set_condition(value, pattern, fmt)

    def _set_condition(self, value, pattern, fmt):
        if self.text is not None:
            res = re.findall(pattern, self.text)
            if len(res) > 0:
                self.text = self.text.replace(res[0], str(value))
                return
        self.text = str.format(fmt, value)



