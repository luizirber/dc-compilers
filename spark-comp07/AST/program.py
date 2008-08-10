import sys

from AST import ast

class Program(ast):
    def __init__(self, arrayVariable, expr):
        ast.__init__(self, "Program")
        self._kids.append(arrayVariable)
        self._kids.append(expr)

    def genC(self):
        print '#include <stdio.h>'
        print 'int main(int argc, char** argv) {'
        if self._kids[0]:
            # generate code for the declaration of variables
            self._kids[0].genC()

        # generate code for the expression
        sys.stdout.write('printf("%d\\n", ')
        self._kids[1].genC()
        print " );"
        print "return 0;"
        print "}"

    def eval(self):
        return self._kids[1].eval()
