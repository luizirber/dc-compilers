import sys

from AST import Statement

class WriteStatement(Statement):
    def __init__(self, expr):
        self.expr = expr

    def genC(self):
        sys.stdout.write('printf("%d", ')
        self.expr.genC()
        print " );"
