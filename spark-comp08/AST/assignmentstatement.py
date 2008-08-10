import sys

from AST import Statement

class AssignmentStatement(Statement):
    def __init__(self, v, expr):
        Statement.__init__(self, "AssignmentStatement")
        self._kids = [v, expr]

    def genC(self):
        sys.stdout.write(self._kids[0].getName() + " = ")
        self._kids[1].genC()
        sys.stdout.write(";\n")
