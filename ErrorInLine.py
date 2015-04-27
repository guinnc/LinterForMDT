__author__ = 'guinnc'
class ErrorInLine:
    'Stores the original line, the line number, and the error message'

    def __init__(self, originalLine, lineNo, errorMessage):
        'Create a rule with an optional semantics'
        self.original = originalLine
        self.lineNumber = lineNo
        self.error = errorMessage
        self.PRINTED = False

    def __str__(self):
        'a pretty string form of the rule'
        return self.original# + "\t# " + self.error
