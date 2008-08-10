import sys

class Program:
    def __init__(self, arrayVariable, expr):
        self.arrayVariable = arrayVariable
        self.expr = expr

    def genC(self):
        print '#include <stdio.h>'
        print 'int main(int argc, char** argv) {'
        if self.arrayVariable:
            # generate code for the declaration of variables
            for variable in self.arrayVariable:
                variable.genC()
        sys.stdout.write('printf("%d\\n", ')
        self.expr.genC()
        print " );"
        print "return 0;"
        print "}"
