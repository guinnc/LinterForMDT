__author__ = 'guinnc'


from tkinter import *
from ErrorInLine import *
from GrammarRule import *
import tkinter as tk

class Linter:

    def __init__(self, edit1, edit2, lineNo):
        self.created = True
        self.editArea = edit1
        self.errorArea = edit2
        self.lineNumbers = lineNo

    def runLinter(self) :

        insideComment = False
        currentLineComment = False
        previousLineBlank = False;

        originalLines = []
        grammarRules = []
        symbolTable = {}
        grammarTable = {}

        # read in a line
        allLines = self.editArea.get("1.0", "end-1c").split("\n")
        for line in allLines:
            # strip leading and trailing spaces
            line = line.strip();

            # remove blank lines if they are next to other blank lines
            if len(line) <= 1:
                if not previousLineBlank:
                    #print(line)
                    originalLines.append(line)
                    previousLineBlank = True


            # handle multiline comments
            if len(line) > 1:
                if line[0] == '/' and line[1] == '*':
                    insideComment = True
                    currentLineComment = True

                if insideComment:
                    #print(line)
                    originalLines.append(line)
                    previousLineBlank = False



                    # Is grammar rule all in one line?

                    # break into 3 parts
                # check to make sure the rule has ->
                if not insideComment:
                    if "->" in line:
                        LHS = ""
                        RHS = ""
                        SEMANTICS = ""
                        parts = re.split("[->:.]", line)
                        #print(parts)
                        twoParts = []
                        count = 0
                        for part in parts:
                            part = part.strip()
                            if len(part) > 0:
                                if count == 0:
                                    LHS = part
                                    symbolTable[LHS] = LHS
                                elif count == 1:
                                    RHS = part
                                elif count == 2:
                                    SEMANTICS = part
                                else:
                                    print("Too much stuff ('" + part + "') at end of line")
                                    error = ErrorInLine(line, len(originalLines) + 1, "Too much stuff ('" + part + "') at end of line")
                                    originalLines.append(error)
                                count+=1
                        if count == 0:
                            print("Nothing to the left or right of the arrow: " + line)
                            error = ErrorInLine(line, len(originalLines) + 1, "Nothing to the left or right of the arrow.")
                            originalLines.append(error)
                        elif count == 1:
                            print("No content on side of arrow: " + line)
                            error = ErrorInLine(line, len(originalLines) + 1, "No content on side of arrow.")
                            originalLines.append(error)
                        elif count == 2:
                            if ":" in line:
                                error = ErrorInLine(line, len(originalLines), "This line has is expecting semantics.")
                                originalLines.append(error)
                            #print(LHS + " -> " + RHS + ".")
                            else:
                                grammarRule = LHS + " -> " + RHS + "."
                                grammarRules.append(grammarRule)
                                originalLines.append(grammarRule)
                                rule = GrammarRule(LHS, RHS, None, len(originalLines))
                                if LHS in grammarTable:
                                    #print("appending %s" % rule)
                                    oldList = grammarTable[LHS]
                                    oldList.append(rule)
                                    grammarTable[LHS] = oldList
                                else:
                                    #print("appending %s" % rule)
                                    x = []
                                    x.append(rule)
                                    grammarTable[LHS] = x

                        elif count == 3:
                            #print(LHS + " -> " + RHS + " : " + SEMANTICS + ".")
                            grammarRule = LHS + " -> " + RHS + " : " + SEMANTICS + "."
                            grammarRules.append(grammarRule)
                            originalLines.append(grammarRule)
                            rule = GrammarRule(LHS, RHS, SEMANTICS, len(originalLines))
                            if LHS in grammarTable:
                                #print("appending %s" % rule)
                                oldList = grammarTable[LHS]
                                oldList.append(rule)
                                grammarTable[LHS] = oldList
                            else:
                                #print("appending %s" % rule)
                                x = []
                                x.append(rule)
                                grammarTable[LHS] = x
                                #print("Table now holds %s" % grammarTable[LHS])


                    else:
                        print("The line '" + line + "' does not have an arrow.")
                        error = ErrorInLine(line, len(originalLines) + 1, "This rule does not have an arrow ->")
                        originalLines.append(error)

                if line[-2] == '*' and line[-1] == '/':
                    insideComment = False
                    currentLineComment = False




        #for key in grammarTable:
        #    for r in grammarTable[key]:
        #        print(r)

        def isComment(line):
            firstSymbol = line.split()[0]
            firstSymbol = firstSymbol.strip()
            try:
                value = grammarTable[firstSymbol]
            except KeyError:
                return True
            return False

        orderedLines = [] # a list containing each line in the reordered file

        #code to rearrange rules so that Non-terminals with the same name
        # are defined sequentially
        previousLineBlank = False
        errorMessages = []
        for count in range(len(originalLines)):
            currentRule = count + 1
            line = originalLines[count]
            if type(line) is ErrorInLine:
                line.lineNumber = len(orderedLines) + 1
                orderedLines.append(line)
                errorMessages.append(line)
            elif len(line.strip()) < 2:
                # grab the last line in orderedLines
                lastLine =  orderedLines[-1]
                if (type(lastLine) is str and len(lastLine.strip()) < 2):
                    previousLineBlank = True
                if not previousLineBlank:
                    orderedLines.append(line) #print(line)
                previousLineBlank = True
            elif isComment(line):
                orderedLines.append(line) #print(line)
            else:
                for key in grammarTable:
                    for r in grammarTable[key]:
                        if r.RULE_NUMBER == currentRule:
                            if not r.PRINTED:
                                orderedLines.append(r) #print(r)
                                r.PRINTED = True
                                previousLineBlank = False
                                # print remaining rules with this key
                                for r2 in grammarTable[key]:
                                    if not r2.PRINTED:
                                        orderedLines.append(r2) # print(r2)
                                        r2.PRINTED = True
                                        previousLineBlank = False

                                orderedLines.append(" ") #print()

        #get rid of two blank lines in a row
        removeExtraNewLines = []
        previousLineBlank = False
        for line in orderedLines:
            if type(line) is str and len(line.strip()) < 2 and previousLineBlank:
                previousLineBlank = True
            else:
                if type(line) is str and len(line.strip()) < 2:
                    previousLineBlank = True
                else:
                    previousLineBlank = False
                removeExtraNewLines.append(line)

        orderedLines = removeExtraNewLines


        #print out orderedLines
        for line in orderedLines:
            print(line)


        #second pass, see if all variables on RHS are in the grammar table
        countLines = 0
        for line in orderedLines:
            countLines += 1
            if type(line) is GrammarRule:
                theRHS = line.RHS
                tokens = theRHS.split()
                variables = []
                for token in tokens:
                    firstChar = token[0]
                    if firstChar.isupper():
                        variables.append(token.strip())

                variablesInSemantics = []
                semantics = line.SEMANTICS
                if not semantics is None:
                    tokens = re.split(r"[\(\), .]", semantics)
                    for token in tokens:
                        if not token.strip() == "":
                            firstChar = token[0]
                            if firstChar.isupper():
                                variablesInSemantics.append(token.strip())

                # make sure that if a variable with a ' on the end in the RHS
                # it must appear in the semantics
                for rhsVariable in variables:
                    lastChar = rhsVariable[-1]
                    if lastChar == "'":
                        if not rhsVariable in variablesInSemantics:
                            line.error = "The non-terminal " + rhsVariable + " on the RHS does not appear in the semantics."
                            error = ErrorInLine(line, countLines, "The non-terminal " + rhsVariable + " on the RHS does not appear in the semantics.")
                            errorMessages.append(error)

                # the converse must also be true.
                for lhsVariable in variablesInSemantics:
                    lastChar = lhsVariable[-1]
                    if lastChar == "'":
                        if not lhsVariable in variables:
                            line.error = "The non-terminal " + lhsVariable + " in the semantics does not appear in the RHS."
                            error = ErrorInLine(line, countLines, "The non-terminal " + lhsVariable + " in the semantics does not appear in the RHS.")
                            errorMessages.append(error)


                removePunctuation = []
                exclude = set("'?!")
                for variable in variables:
                    s = ''.join(ch for ch in variable if ch not in exclude)
                    removePunctuation.append(s)
                #print(removePunctuation)

                if not removePunctuation == []:
                    # look up each token
                    for variable in removePunctuation:
                        try:
                            rule = grammarTable[variable]
                            if rule is None:
                                line.error = "The non-terminal '" + variable + "' has no corresponding rules."
                                error = ErrorInLine(line, countLines, "The non-terminal '" + variable + "' has no corresponding rules.")
                                errorMessages.append(error)
                        except KeyError:
                            line.error = "The non-terminal '" + variable + "' has no corresponding rules."
                            error = ErrorInLine(line, countLines, "The non-terminal '" + variable + "' has no corresponding rules.")
                            errorMessages.append(error)


        #clear editArea, lineNumbers, and errorArea
        self.editArea.delete(1.0, tk.END)
        self.lineNumbers.delete(1.0, tk.END)
        self.errorArea.delete(1.0, tk.END)
        count = 1;
        for line in orderedLines:
            self.editArea.insert(tk.INSERT, line)
            self.editArea.insert(tk.INSERT, "\n")
            self.lineNumbers.insert(tk.INSERT, str(count))
            self.lineNumbers.insert(tk.INSERT, "\n")
            count += 1

        if errorMessages == []:
            print("\nStatistics")
            print("Number of Grammar Rules: " + str(len(grammarRules)))
            print("Number of Non-terminal symbols: " + str(len(symbolTable)))
            self.errorArea.insert(tk.INSERT, "No errors\n")
            self.errorArea.insert(tk.INSERT, "Statistics\n")
            self.errorArea.insert(tk.INSERT, "Number of Grammar Rules: " + str(len(grammarRules)) + "\n")
            self.errorArea.insert(tk.INSERT, "Number of Non-terminal symbols: " + str(len(symbolTable)) + "\n")
        else:
            for error in errorMessages:
                self.errorArea.insert(tk.INSERT, "ERROR: Line " + str(error.lineNumber) + ": ")
                self.errorArea.insert(tk.INSERT, error.error)
                self.errorArea.insert(tk.INSERT, "\n")

                self.editArea.tag_add("start", str(error.lineNumber) + ".0", str(error.lineNumber) + ".400")
                self.editArea.tag_config("start", background="pink", foreground="black")



    def printError(linesSoFar, errorMessage):
        for line in linesSoFar:
            print(line)
        print(errorMessage);
