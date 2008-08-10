#
#  comp7
#
#  Class CompilerRuntime models the runtime system. Its method 'error'
#  signals a error at runtime and terminates the program.
#
#  Class Expr and its subclasses now have a method 'eval' to evaluate the
#  expression. An expression can be a letter whose value was previously
#  assigned before the ':' --- see the grammar. Then it is necessary to use
#  a symbol table to keep the variables with its values. The Symbol Table is
#  pointed by variable symbolTable
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

    symbolTable = {}

    def compile(self, p_input):
        self.input = p_input
        self.tokenPos = 0
        self.nextToken()
        result = self.program()
        if self.token != '\0':
            self.error("End of file expected")
        return result

    def program(self):
        arrayVariable = self.varDecList()
        if self.token != ':':
            self.error(': expected')
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
            self.error("=  expected")
            return None
        else:
            self.nextToken()
            n = self.number()
            # semantic analysis
            # inserts the variable in the Symbol Table. It will be used to
            # retrieve the value of the variable when it is found inside the
            # expression and to check if the variable found in the expression
            # was 'declared' before the ':'
            try:
                self.symbolTable[name]
            except KeyError:
                self.symbolTable[name] = n
            else:
                self.error("Variable " + name + " has already been declared")
            return Variable(name, n.getValue())

    def letter(self):
        if not self.token.isalpha():
            self.error("Letter expected")
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
                self.error(") expected")
            return ce
        else:
            # Note we test the token to decide which production to use
            if self.token.isdigit():
                return self.number()
            else:
                return self.letterExpr()

    def number(self):
        if self.token >= '0' and self.token <= '9':
            e = NumberExpr(self.token)
            self.nextToken()
            return e
        else:
            self.error()

    def letterExpr(self):
        ch = self.letter()
        # semantic analysis
        # was the variable declared?
        try:
            e = self.symbolTable[ch]
        except KeyError:
            self.error("Variable was not declared")
        else:
            return VariableExpr(ch, e.getValue())

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

    def error(self, message):
        if self.tokenPos == 0:
            self.tokenPos = 1
        else:
            if self.tokenPos >= len(self.input):
                self.tokenPos = len(self.input)

            strInput = self.input[self.tokenPos - 1:self.tokenPos]
            strError = 'Error at "' + strInput + '"'

            raise Exception(strError + " -> " + message)
