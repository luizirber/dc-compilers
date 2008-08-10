import sys

from AST import Statement

class IfStatement(Statement):
    def __init__(self, expr, thenPart, elsePart):
        Statement.__init__(self, "IfStatement")
        # _kids[0] = expr
        # _kids[1] = thenPart
        # _kids[2] = elsePart
        self._kids = [expr, thenPart, elsePart]

    def genC(self):
       sys.stdout.write("if ( ")
       self._kids[0].genC()
       sys.stdout.write(" ) {\n")
       if self._kids[1]:
           self._kids[1].genC()
       sys.stdout.write("}\n")
       if self._kids[2]:
           sys.stdout.write("else {\n")
           self._kids[2].genC()
           sys.stdout.write("}\n")

