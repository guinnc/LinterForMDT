__author__ = 'guinnc'

class GrammarRule:
    'Stores the left hand side, right hand side, and optional semantics'

    def __init__(self, lhsArg, rhsArg, semArg=None, ruleNo=1, print=False):
        'Create a rule with an optional semantics'
        self.LHS = lhsArg
        self.RHS = rhsArg
        self.SEMANTICS = semArg
        self.RULE_NUMBER = ruleNo
        self.PRINTED = print
        self.ERROR = ""

    def __str__(self):
        'a pretty string form of the rule'
        if self.SEMANTICS is None:
            return '%s -> %s.' % (self.LHS, self.RHS)
        else:
            return '%s -> %s : %s.' % (self.LHS, self.RHS, self.SEMANTICS)


