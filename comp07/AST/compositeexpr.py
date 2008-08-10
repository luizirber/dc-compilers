import sys

from AST import Expr, CompilerRuntime

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

    def eval(self):
        evalLeft = self.left.eval()
        evalRight = self.right.eval()

        if self.oper == '+':
            return evalLeft + evalRight
        elif self.oper == '-':
            return evalLeft - evalRight
        elif self.oper == '*':
            return evalLeft * evalRight
        elif self.oper == '/':
            if evalRight == 0:
                CompilerRuntime.error("Division by zero")
            return evalLeft / evalRight
        else:
            CompilerRuntime.error("Unknown operator")
            return 0
