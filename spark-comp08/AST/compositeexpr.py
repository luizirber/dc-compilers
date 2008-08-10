import sys

from AST import Expr

class CompositeExpr(Expr):
    def __init__(self, pleft, poper, pright):
        Expr.__init__(self, 'CompositeExpr')
        # _kids[0] = pleft
        # _kids[1] = pright
        self._kids.append(pleft)
        self._kids.append(pright)
        self.attr = poper

    def genC(self):
        sys.stdout.write("(")
        self._kids[0].genC()
        sys.stdout.write(" " + self.attr + " ")
        self._kids[1].genC()
        sys.stdout.write(")")

