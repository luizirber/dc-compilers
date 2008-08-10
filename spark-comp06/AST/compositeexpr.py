import sys

from AST import Expr

class CompositeExpr(Expr):
    def __init__(self, pleft, poper, pright):
        self.left = pleft
        self.oper = poper
        self.right = pright

    def genC(self):
        sys.stdout.write("(")
        self.left.genC()
        sys.stdout.write(" " + self.oper + " ")
        self.right.genC()
        sys.stdout.write(")")
