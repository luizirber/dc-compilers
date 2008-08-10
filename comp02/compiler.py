#
#  comp2
#  This program is a synthatic analyzer and code generator for
#  the following grammar:
#
#  Expr ::= '(' oper Expr Expr ')' | number
#  oper ::= '+' | '-'
#  number ::= '0' | '1' | ... | '9'
#
#  The code is generated to C

import sys

class Compiler:
    def compile(self, p_input):
        self.input = p_input
        self.tokenPos = 0
        self.nextToken()
        self.expr()
        print
        if self.token != '\0':
            self.error()

    def expr(self):
        if self.token == '(':
            self.nextToken()
            op = self.oper()
            sys.stdout.write("(")
            self.expr()
            sys.stdout.write(op)
            self.expr()
            sys.stdout.write(")")
            if self.token == ')':
                self.nextToken()
            else:
                self.error()
        else:
            self.number()

    def number(self):
        if self.token >= '0' and self.token <= '9':
            sys.stdout.write(self.token)
            self.nextToken()
        else:
            self.error()

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
