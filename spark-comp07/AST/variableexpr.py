import sys

from AST import Expr

class VariableExpr(Expr):
    def __init__(self, name, value):
        Expr.__init__(self, "VariableExpr")
        self.name = name
        self.value = value

    def __str__(self):
        return str(self.name)

    def genC(self):
        sys.stdout.write(self.name)

    def eval(self):
        return self.value
