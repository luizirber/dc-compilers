import sys

from AST import Expr

class NumberExpr(Expr):
    def __init__(self, n):
        Expr.__init__(self, "NumberExpr")
        self.value = int(n)

    def genC(self):
        sys.stdout.write(self.attr)

    def getValue(self):
        return self.value

