from FileModel.Block import Block


def count_body(body):
    return sum([count_block(m) if type(m) is Block else count_text(m) for m in body])


def count_branch(branch):
    return sum([count_text(branch.condition.text), count_body(branch.body)])


def count_block(block):
    return sum([count_branch(b) for b in block.branches] + [count_text(block.end)])


def count_text(text):
    return len([l for l in text.split('\n') if l])

