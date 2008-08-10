import sys

from AST import ast

class Program(ast):
    def __init__(self, arrayVariable, statementList):
        ast.__init__(self, "Program")
        self._kids = [arrayVariable, statementList]

    def genC(self):
        print '#include <stdio.h>'
        print 'int main(int argc, char** argv) {'
        if self._kids[0]:
            # generate code for the declaration of variables
            self._kids[0].genC()

        # generate code for the statements
        if self._kids[1]:
            self._kids[1].genC()
        print "return 0;"
        print "}"

