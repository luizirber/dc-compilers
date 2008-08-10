import sys

from AST import Expr, CompilerRuntime

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

    def eval(self):
        evalLeft = self._kids[0].eval()
        evalRight = self._kids[1].eval()

        if self.attr == '+':
            return evalLeft + evalRight
        elif self.attr == '-':
            return evalLeft - evalRight
        elif self.attr == '*':
            return evalLeft * evalRight
        elif self.attr == '/':
            if evalRight == 0:
                CompilerRuntime.error("Division by zero")
            return evalLeft / evalRight
        else:
            CompilerRuntime.error("Unknown operator")
            return 0
