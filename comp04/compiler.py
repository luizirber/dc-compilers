#
#  comp4
#  This program is a synthatic analyzer and code generator for
#  the following grammar:
#
#  Expr ::= '(' oper Expr Expr ')' | number
#  oper ::= '+' | '-'
#  number ::= '0' | '1' | ... | '9'
#
#  The code is generated to C

class Compiler:
    def compile(self, p_input):
        self.input = p_input
        self.tokenPos = 0
        self.nextToken()
        result = self.expr()
        if self.token != '\0':
            self.error()
        return result

    def expr(self):
        if self.token == '(':
            self.nextToken()
            op = self.oper()
            left = self.expr()
            right = self.expr()
            result = 0
            if op == '+':
                result = left + right
            elif op == '-':
                result = left - right
            if self.token == ')':
                self.nextToken()
            else:
                self.error()
            return result
        else:
            return self.number()

    def number(self):
        result = 0
        if self.token >= '0' and self.token <= '9':
            result = int(self.token)
            self.nextToken()
        else:
            self.error()
        return result

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
