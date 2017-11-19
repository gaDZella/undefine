from FileModel.FragmentType import FragmentType
from FileModel.Branch import Branch
from FileModel.ConditionBlock import ConditionBlock


class BlockModelBuilder:
    Terminators = [FragmentType.ElseStatement, FragmentType.ElIfStatement, FragmentType.EndIfStatement]

    @staticmethod
    def build(model):
        it = BlockModelBuilder._create_iterator(model)
        yield from BlockModelBuilder._build(it)

    @staticmethod
    def _build(it):
        f = next(it, None)
        while f is not None:
            if f.type in BlockModelBuilder.Terminators:
                break
            if f.type == FragmentType.IfStatement:
                yield BlockModelBuilder._build_block(it, f)
            elif f.type != FragmentType.Body:
                raise Exception()
            else:
                yield f.text
            f = next(it, None)

    @staticmethod
    def _build_block(it, if_f):
        start_cond = if_f
        start_body = list(BlockModelBuilder._build(it))
        f = it.current
        next_branches = []
        while f is not None and f.type != FragmentType.EndIfStatement:
            if f.type == FragmentType.Body:
                raise Exception()
            cond = f
            body = list(BlockModelBuilder._build(it))
            f = it.current
            next_branches.append(Branch(cond, body))
        if f.type != FragmentType.EndIfStatement:
            raise Exception()
        return ConditionBlock(Branch(start_cond, start_body), next_branches, f.text)

    @staticmethod
    def _next_not_last(it):
        f = next(it)
        if f is None:
            raise Exception()
        return f

    @staticmethod
    def _create_iterator(list):
        return WithCurrentGen(iter(list))


class WithCurrentGen(object):

    def __init__(self, it):
        self.__it = it

    def __iter__(self):
        return self

    def __next__(self):
        self.current = next(self.__it)
        return self.current

    def __call__(self):
        return self







