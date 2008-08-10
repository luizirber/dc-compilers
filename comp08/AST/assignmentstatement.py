import sys

from AST import Statement

class AssignmentStatement(Statement):
    def __init__(self, v, expr):
        self.v = v
        self.expr = expr

    def genC(self):
        sys.stdout.write(self.v.getName() + " = ")
        self.expr.genC()
        sys.stdout.write(";\n")
