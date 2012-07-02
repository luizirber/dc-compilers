#
#  comp6
#
#  We added to the grammar more operators and a declaration of variables so
#  the grammar now accepts a program like
#      a = 1 b = 3 : (- (+ a 2) 3)
#  The result of the evaluation would be 0. Another program would be
#      g = 3 t = 9 : (* (- t 7) g)
#
#  Of course, the AST was extended to cope with the new rules. New classes
#  were created:
#      Program - represents the program
#      Variable - a variable in the declaration
#      VariableExpr - a variable inside an expression
#
#  Grammar:
#      Program ::= VarDecList ':' Expr
#      VarDecList ::= | VarDec VarDecList
#      VarDec ::= Letter '=' Number
#      Expr ::= '(' Oper Expr Expr ')' | Number | Letter
#      Oper ::= '+' | '-' | '*' | '/'
#      Number ::= '0' | '1' | ... | '9'
#      Letter ::= 'A' | 'B' | ... | 'Z' | 'a'| 'b' | ... | 'z'

import sys

from AST import (Expr, CompositeExpr, NumberExpr,
                 Variable, VariableExpr, Program)

class Compiler:
    def compile(self, p_input):
        self.input = p_input
        self.tokenPos = 0
        self.nextToken()
        result = self.program()
        print self.token
        if self.token != '\0':
            self.error()
        return result

    def program(self):
        arrayVariable = self.varDecList()
        if self.token != ':':
            self.error()
            return None
        else:
            self.nextToken()
            e = self.expr()
            return Program(arrayVariable, e)

    def varDecList(self):
        ''' See how the repetition in the grammar reflects in the code.
            Since VarDec always begin with a letter, if token is NOT a
            letter, then VarDecList is empty and None is returned'''
        if not self.token.isalpha():
            return None
        else:
            arrayVariable = []
            while self.token.isalpha():
                arrayVariable.append( self.varDec() )
            return arrayVariable

    def varDec(self):
        name = self.letter()
        if self.token != '=':
            self.error()
            return None
        else:
            self.nextToken()
            n = self.number()
            return Variable(name, n.getValue())

    def letter(self):
        if not self.token.isalpha():
            self.error()
        else:
            ch = self.token
            self.nextToken()
            return ch

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
            # Note we test the token to decide which production to use
            if self.token.isdigit():
                return self.number()
            else:
                return VariableExpr(self.letter())

    def number(self):
        if self.token >= '0' and self.token <= '9':
            e = NumberExpr(self.token)
            self.nextToken()
            return e
        else:
            self.error()

    def oper(self):
        op = self.token
        if (self.token == '+' or self.token == '-'
            or self.token == '*' or self.token == '/'):
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
