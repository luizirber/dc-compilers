import sys

from AST import Expr
from Lexer import Symbol

class CompositeExpr(Expr):
    def __init__(self, pleft, poper, pright):
        self.left = pleft
        self.oper = poper
        self.right = pright

        self.strOper = {
            Symbol.PLUS   : "+",
            Symbol.MINUS  : "-",
            Symbol.MULT   : "*",
            Symbol.DIV    : "/",
            Symbol.LT     : "<",
            Symbol.LE     : "<=",
            Symbol.GT     : ">",
            Symbol.GE     : ">=",
            Symbol.NEQ    : "!=",
            Symbol.EQ     : "==",
            Symbol.ASSIGN : "="
        }

    def genC(self):
        sys.stdout.write("(")
        self.left.genC()
        sys.stdout.write(" " + self.strOper[self.oper] + " ")
        self.right.genC()
        sys.stdout.write(")")

