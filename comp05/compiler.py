#
#  comp5
#  This program is a synthatic analyzer that builds the abstract syntax tree
#  (AST). The classes of the AST were put in the module AST. The classes of the
#  AST represent expressions and all have a 'genC' method. If exp is a variable
#  of class Expr, then
#      exp.genC()
#  generates code in C for the expression.
#
#  Grammar:
#
#      Expr ::= '(' oper Expr Expr ')' | number
#      oper ::= '+' | '-'
#      number ::= '0' | '1' | ... | '9'

import sys

from AST import Expr, CompositeExpr, NumberExpr

class Compiler:
    def compile(self, p_input):
        self.input = p_input
        self.tokenPos = 0
        self.nextToken()
        e = self.expr()
        if self.token != '\0':
            self.error()
        return e

    def expr(self):
        if self.token == '(':
            self.nextToken()
            op = self.oper()
            e1 = self.expr()
            e2 = self.expr()
            ce = CompositeExpr(e1, op, e2)
            if self.token == ')':
                self.nextToken()
            else:
                self.error()
            return ce
        else:
            return self.number()

    def number(self):
        if self.token >= '0' and self.token <= '9':
            e = NumberExpr(self.token)
            self.nextToken()
        else:
            self.error()
        return e

    def oper(self):
        op = self.token
        if self.token == '+' or self.token == '-':
            self.nextToken()
            return op
        else:
            self.error()

    def nextToken(self):
        while self.tokenPos < len(self.input) and self.input[self.tokenPos] == " ":
            self.tokenPos += 1
        if self.tokenPos < len(self.input):
            self.token = self.input[self.tokenPos]
            self.tokenPos += 1
        else:
            self.token = '\0'

    def error(self):
        if self.tokenPos == 0:
            self.tokenPos = 1
        else:
            if self.tokenPos >= len(self.input):
                self.tokenPos = len(self.input)

            strInput = self.input[self.tokenPos - 1:self.tokenPos]
            strError = 'Error at "' + strInput + '"'

            raise Exception(strError)
