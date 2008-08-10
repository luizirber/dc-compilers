import sys

class Program:
    def __init__(self, arrayVariable, statementList):
        self.arrayVariable = arrayVariable
        self.statementList = statementList

    def genC(self):
        print '#include <stdio.h>'
        print 'int main(int argc, char** argv) {'
        if self.arrayVariable:
            # generate code for the declaration of variables
            for variable in self.arrayVariable:
                variable.genC()

        # generate code for the expression
        self.statementList.genC()
        print "return 0;"
        print "}"
