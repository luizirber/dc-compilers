import sys

from AST import Expr

class VariableExpr(Expr):
    def __init__(self, name):
        self.name = name

    def genC(self):
        sys.stdout.write(self.name)
