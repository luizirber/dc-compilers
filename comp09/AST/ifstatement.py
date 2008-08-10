import sys

from AST import Statement

class IfStatement(Statement):
    def __init__(self, expr, thenPart, elsePart):
        self.expr = expr
        self.thenPart = thenPart
        self.elsePart = elsePart

    def genC(self):
       sys.stdout.write("if ( ")
       self.expr.genC()
       sys.stdout.write(" ) {\n")
       if self.thenPart:
           self.thenPart.genC()
       sys.stdout.write("}\n")
       if self.elsePart:
           sys.stdout.write("else {\n")
           self.elsePart.genC()
           sys.stdout.write("}\n")

