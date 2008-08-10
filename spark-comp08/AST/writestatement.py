import sys

from AST import Statement

class WriteStatement(Statement):
    def __init__(self, expr):
        Statement.__init__(self, "WriteStatement")
        self._kids = [expr]

    def genC(self):
        sys.stdout.write('printf("%d", ')
        self._kids[0].genC()
        print " );"
