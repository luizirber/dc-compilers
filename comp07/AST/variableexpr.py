import sys

from AST import Expr

class VariableExpr(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def genC(self):
        sys.stdout.write(self.name)

    def eval(self):
        return self.value
