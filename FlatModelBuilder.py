import re
from Model.Fragment import Fragment
from Model.FragmentType import FragmentType


MiltilineCommentP = r"/\*(?:\n|.)+?\*/"
LineCommentP = r"//.+?(?:\n|$)"
IfStatementP = r"[ \t\f]*#[ \t\f]*if\s*.+?(?:\n|$)"
ElifStatementP = r"[ \t\f]*#[ \t\f]*elif\s*.+?(?:\n|$)"
ElseStatementP = r"[ \t\f]*#[ \t\f]*else\s*?(?:\n|$)"
EndIfStatementP = r"[ \t\f]*#[ \t\f]*endif\s*?(?:\n|$)?"


def build(file):
    model = split_recursive(file, [
        (MiltilineCommentP, FragmentType.Body),
        (LineCommentP, FragmentType.Body),
        (IfStatementP, FragmentType.IfStatement),
        (ElifStatementP, FragmentType.ElIfStatement),
        (ElseStatementP, FragmentType.ElseStatement),
        (EndIfStatementP, FragmentType.EndIfStatement),
    ])
    return _normalize(model)


def split_recursive(file, patterns):
    res = [Fragment(FragmentType.Body, file)]
    left_count = len(patterns)
    if left_count is not 0:
        res = []
        pattern = patterns[0]
        split_result = re.split(str.format("({0})", pattern[0]), file)

        for fragment in split_result:
            if len(fragment) == 0:
                continue
            if re.match(pattern[0], fragment) is None:
                res.extend(
                    split_recursive(fragment, patterns[1:]))
            else:
                res.append(Fragment(pattern[1], fragment))
    return res


def _normalize(model):
    res = []
    body_text = None
    for fragment in model:
        if fragment.type == FragmentType.Body:
            prev_text = body_text if body_text is not None else ''
            body_text = prev_text + fragment.text
        else:
            if body_text is not None:
                res.append(Fragment(FragmentType.Body, body_text))
                body_text = None
            res.append(fragment)
    if body_text is not None:
        res.append(Fragment(FragmentType.Body, body_text))
    return res
