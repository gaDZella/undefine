from Model.FragmentType import FragmentType
from Model.Block import Block
from Model import ConditionAccessor
from CleanResult import CleanResult
import Condition
import LineCounter


def process(model, keys):
    res = CleanResult("", None, 0, 0)
    _process_body(model, res, keys)
    return res


def _process_body(body, res, keys):
    for m in body:
        if type(m) is Block:
            _process_block(m, res, keys)
        else:
            res.text += m


def _process_block(b, res, keys):
    branches = b.branches
    count = len(branches)
    last_cond = True
    for i in range(0, count):
        branch = branches[i]
        cond = _patch_cond(branch.condition, keys, last_cond)
        if type(cond) is bool:
            if i == 0:
                if cond:
                    _process_body(branch.body, res, keys)
                else:
                    res.code_lines += LineCounter.count_body(branch.body)
                if count > 1:
                    next_f = branches[i + 1].condition
                    next_cond = _patch_cond(next_f, keys, cond)
                    next_f.type = FragmentType.IfStatement
                    ConditionAccessor.set_condition(next_f, next_cond)
                    _process_block(Block(branches[i + 1:], b.end), res, keys)
                    return
            else:
                if cond:
                    res.code_lines += sum([LineCounter.count_body(b.body) for b in branches[i + 1:]])
                    if branch.condition.type == FragmentType.ElseStatement:
                        res.text += "#endif\n"
                        _process_body(branch.body, res, keys)
                        return
                    res.text += "#else\n"
                    _process_body(branch.body, res, keys)
                    break
                else:
                    res.code_lines = LineCounter.count_body(branch.body)

        else:
            res.text += branch.condition.text
            _process_body(branch.body, res, keys)
        last_cond = cond
    if type(last_cond) is not bool or count > 1:
        res.text += b.end


def _patch_cond(f, keys, prev_cond):
    if f.type == FragmentType.ElseStatement:
        cond = str.format("!({})", prev_cond)
    else:
        cond = ConditionAccessor.get_condition(f)
    patched_cond = Condition.simplify(cond, keys)
    if patched_cond is not cond:
        ConditionAccessor.set_condition(f, patched_cond)
    return patched_cond
