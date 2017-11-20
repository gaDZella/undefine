from FileModel.FragmentType import FragmentType
from FileModel.Branch import Branch
from FileModel.ConditionBlock import ConditionBlock


class WithCurrentIter(object):

    def __init__(self, it):
        self.__it = it

    def __iter__(self):
        return self

    def __next__(self):
        self.current = next(self.__it)
        return self.current

    def __call__(self):
        return self


Block_terminators = [
    FragmentType.ElseStatement,
    FragmentType.ElIfStatement,
    FragmentType.EndIfStatement
]


def build(model):
    it = _create_iterator(model)
    yield from _build(it)


def _build(it):
    f = next(it, None)
    while f is not None:
        if f.type in Block_terminators:
            break
        if f.type == FragmentType.IfStatement:
            yield _build_block(it, f)
        elif f.type != FragmentType.Body:
            raise Exception()
        else:
            yield f.text
        f = next(it, None)


def _build_block(it, if_f):
    start_cond = if_f
    start_body = list(_build(it))
    f = it.current
    next_branches = []
    while f is not None and f.type != FragmentType.EndIfStatement:
        if f.type == FragmentType.Body:
            raise Exception()
        cond = f
        body = list(_build(it))
        f = it.current
        next_branches.append(Branch(cond, body))
    if f.type != FragmentType.EndIfStatement:
        raise Exception()
    return ConditionBlock(Branch(start_cond, start_body), next_branches, f.text)


def _create_iterator(obj):
    return WithCurrentIter(iter(obj))










