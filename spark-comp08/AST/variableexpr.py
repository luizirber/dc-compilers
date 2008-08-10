import sys

from AST import Expr

class VariableExpr(Expr):
    def __init__(self, v):
        Expr.__init__(self, "VariableExpr")
        self._kids = [v]

    def __str__(self):
        return str(self.name)

    def genC(self):
        sys.stdout.write(self._kids[0].getName())

