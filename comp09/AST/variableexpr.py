import sys

from AST import Expr

class VariableExpr(Expr):
    def __init__(self, v):
        self.v = v

    def genC(self):
        sys.stdout.write(self.v.getName())

