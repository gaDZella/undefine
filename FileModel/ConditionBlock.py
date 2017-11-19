class ConditionBlock:

    def __init__(self, start_branch, next_branches, end_fragment):
        self.start = start_branch
        self.next = next_branches
        self.end = end_fragment
