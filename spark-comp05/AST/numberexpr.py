import sys

from AST import Expr

class NumberExpr(Expr):
    def __init__(self, n):
        self.n = n

    def genC(self):
        sys.stdout.write(self.n)
