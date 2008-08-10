#
#  comp8
#
#  Variables now can have any number of characters and numbers any number of
#  digits. There are new keywords and new non-terminals. The operator set
#  includes the comparison operators. There are a few statements.
#  Anything after // till the end of the line is a comment.
#
#  The input is now taken from a file.
#  Method error now prints the line in which the error occurred.

#  Grammar:
#      Program ::= [ 'var' VarDecList ';' ] CompositeStatement
#      CompositeStatement ::= 'begin' StatementList 'end'
#      StatementList ::= | Statement ';' StatementList
#      Statement ::= AssignmentStatement | IfStatement | ReadStatement | WriteStatement
#      AssignmentStatement ::= Variable '=' Expr
#      IfStatement ::= 'if' Expr 'then' StatementList [ 'else' StatementList ] 'endif'
#      ReadStatement ::= 'read' '(' Variable ')'
#      WriteStatement ::= 'write' '(' Expr ')'

#      Variable ::= Letter { Letter }
#      VarDecList ::= Variable | Variable ',' VarDecList
#      Expr ::= '(' Oper Expr Expr ')' | Number | Variable
#      Oper ::= '+' | '-' | '*' | '/' | '<' | '<=' | '>' | '>=' | '==' | '<>'
#      Number ::= Digit { Digit }
#      Number ::= '0' | '1' | ... | '9'
#      Letter ::= 'A' | 'B' | ... | 'Z' | 'a'| 'b' | ... | 'z'
#
#  Anything between [] is optional. Anything between { and } can be repeated
#  zero or more times.

import sys

from AST import (Expr, CompositeExpr, NumberExpr, Variable, VariableExpr,
                 Program, AssignmentStatement, ReadStatement, WriteStatement,
                 StatementList, IfStatement)

from Lexer import Symbol

class Compiler:

    keywordsTable = {}
    maxValueInteger = 32768
    lineNumber = 1

    def __init__(self):
        self.keywordsTable["var"]   = Symbol.VAR
        self.keywordsTable["begin"] = Symbol.BEGIN
        self.keywordsTable["end"]   = Symbol.END
        self.keywordsTable["if"]    = Symbol.IF
        self.keywordsTable["then"]  = Symbol.THEN
        self.keywordsTable["else"]  = Symbol.ELSE
        self.keywordsTable["endif"] = Symbol.ENDIF
        self.keywordsTable["read"]  = Symbol.READ
        self.keywordsTable["write"] = Symbol.WRITE

    def compile(self, p_input):
        self.input = p_input
        # add an end-of-file label to make it easy to do the lexer
        #self.input[len(self.input)] = '\0'

        # number of the current line
        self.lineNumber = 1
        self.tokenPos = 0

        # symbol table. Will contain the declared variables
        self.symbolTable = {}
        self.nextToken()
        return self.program()

    def program(self):
        """ Program ::= [ 'var' VarDecList ] CompositeStatement """
        arrayVariable = None
        if self.token == Symbol.VAR:
            self.nextToken()
            arrayVariable = self.varDecList()
            if self.token != Symbol.SEMICOLON:
                self.error('; expected')
            self.nextToken()

        program = Program(arrayVariable, self.compositeStatement())
        if self.token != Symbol.EOF:
            self.error("EOF expected")
        return program

    def compositeStatement(self):
        """ CompositeStatement ::= 'begin' StatementList 'end'
            StatementList ::= | Statement ';' StatementList """
        if self.token != Symbol.BEGIN:
            self.error('"begin" expected')
        self.nextToken()
        sl = self.statementList()
        if self.token != Symbol.END:
            self.error('"end" expected')
        self.nextToken()
        return sl

    def statementList(self):
        v = []
        while (self.token == Symbol.IDENT or
               self.token == Symbol.IF or
               self.token == Symbol.READ or
               self.token == Symbol.WRITE):
            v.append(self.statement())
            if self.token != Symbol.SEMICOLON:
                self.error("; expected")
            self.nextToken()
        return StatementList(v)

    def statement(self):
        """ Statement ::= AssignmentStatement | IfStatement | ReadStatement |
                          WriteStatement """
        if self.token == Symbol.IDENT:
            return self.assignmentStatement()
        elif self.token == Symbol.IF:
            return self.ifStatement()
        elif self.token == Symbol.READ:
            return self.readStatement()
        elif self.token == Symbol.WRITE:
            return self.writeStatement()
        else:
            # will never be executed
            self.error("Statement expected")

    def assignmentStatement(self):
        # the current token is Symbol.IDENT and stringValue contains the
        # identifier
        name = self.stringValue

        # is the variable in the symbol table? Variables are inserted in the
        # symbol table when they are declared. If the variable is not there, it
        # has not been declared.
        try:
            v = self.symbolTable[name]
        except KeyError:
            # it wasn't in the symbol table
            self.error("Variable " + name + " was not declared")
        # eat token Symbol.IDENT
        self.nextToken()
        if self.token != Symbol.ASSIGN:
            self.error("= expected")
        self.nextToken()
        return AssignmentStatement(v, self.expr())

    def ifStatement(self):
        self.nextToken()
        e = self.expr()
        if self.token != Symbol.THEN:
            self.error('"then" expected')
        self.nextToken()
        thenPart = self.statementList()
        elsePart = None
        if self.token == Symbol.ELSE:
            self.nextToken()
            elsePart = self.statementList()
        if self.token != Symbol.ENDIF:
            self.error('"endif" expected')
        self.nextToken()
        return IfStatement(e, thenPart, elsePart)

    def readStatement(self):
        self.nextToken()
        if self.token != Symbol.LEFTPAR:
            self.error("( expected")
        self.nextToken()
        if self.token != Symbol.IDENT:
            self.error("Identifier expected")
        # check if the variable was declared
        name = self.stringValue
        try:
            v = self.symbolTable[name]
        except KeyError:
            self.error("Variable " + name + " was not declared")
        self.nextToken()
        if self.token != Symbol.RIGHTPAR:
            self.error(") expected")
        self.nextToken()
        return ReadStatement(v)

    def writeStatement(self):
        self.nextToken()
        if self.token != Symbol.LEFTPAR:
            self.error("( expected")
        self.nextToken()
        e = self.expr()
        if self.token != Symbol.RIGHTPAR:
            self.error(") expected")
        self.nextToken()
        return WriteStatement(e)

    def varDecList(self):
        ''' VarDecList ::= Variable | Variable ',' VarDecList ';' '''
        v = []
        v.append(self.varDec())
        while self.token == Symbol.COMMA:
            self.nextToken()
            v.append(self.varDec())
        return v

    def varDec(self):
        if self.token != Symbol.IDENT:
            self.error("Identifier expected")
        # name of the identifier
        name = self.stringValue
        self.nextToken()

        # semantic analysis
        # if the name is in the symbol table, the variable has been declared
        # twice
        try:
            self.symbolTable[name]
        except KeyError:
            # inserts the variable in the symbol table. The name is the key and
            # an object of class Variable is the value. Dicts store a pair
            # (key,value) retrieved by the key
            self.symbolTable[name] = Variable(name)
        else:
            self.error("Variable " + name + " has already been declared")
        return self.symbolTable[name]

    def expr(self):
        if self.token == Symbol.LEFTPAR:
            self.nextToken()
            op = self.token
            if ( op == Symbol.EQ or op == Symbol.NEQ or op == Symbol.LE or
                 op == Symbol.LT or op == Symbol.GE or op == Symbol.GT or
                 op == Symbol.PLUS or op == Symbol.MINUS or
                 op == Symbol.MULT or op == Symbol.DIV):
                self.nextToken()
            else:
                self.error("operator expected")
            e1 = self.expr()
            e2 = self.expr()
            ce = CompositeExpr(e1, op, e2)
            if self.token == Symbol.RIGHTPAR:
                self.nextToken()
            else:
                self.error(") expected")
            return ce
        else:
            # Note we test the token to decide which production to use
            if self.token == Symbol.NUMBER:
                return self.number()
            else:
                if self.token != Symbol.IDENT:
                    self.error("Identifier expected")
                name = self.stringValue
                self.nextToken()
                # semantic analysis
                # was the variable declared?
                try:
                    v = self.symbolTable[name]
                except KeyError:
                    self.error("Variable " + name + " was not declared")
                return VariableExpr(v)

    def number(self):
        if self.token != Symbol.NUMBER:
            self.error("Number expected") # in the current version, never occurs
        # the number value is stored in numberValue as an int
        value = self.numberValue
        self.nextToken()
        return NumberExpr(value)

    def nextToken(self):
        ch = self.input[self.tokenPos]
        while ch == ' ' or ch == '\r' or ch == '\t' or ch == '\n':
            # count the number of lines
            if ch == '\n':
                self.lineNumber += 1
            self.tokenPos += 1
            ch = self.input[self.tokenPos]
        if ch == '\0':
            self.token = Symbol.EOF
        elif (self.input[self.tokenPos] == '/' and
          self.input[self.tokenPos + 1] == '/'):
              # comment found
              while (self.input[self.tokenPos] != '\0' and
                self.input[self.tokenPos] != '\n'):
                  self.tokenPos += 1
              self.nextToken()
        elif ch.isalpha():
            # got an identifier or keyword
            # we put the characters in a list, and when we got them all
            # we build a string
            ident = []
            while self.input[self.tokenPos].isalpha():
                ident.append(self.input[self.tokenPos])
                self.tokenPos += 1
                # now we build the string
                self.stringValue = ''.join(ident)
                # if it is in the list of keywords, it is a keyword
                try:
                    value = self.keywordsTable[self.stringValue]
                except KeyError:
                    self.token = Symbol.IDENT
                else:
                    self.token = value
                if self.input[self.tokenPos].isdigit():
                    self.error("Word followed by a number")
        elif ch.isdigit():
            # get a number
            number = []
            while self.input[self.tokenPos].isdigit():
                number.append(self.input[self.tokenPos])
                self.tokenPos += 1
            self.token = Symbol.NUMBER
            self.numberValue = int("".join(number))
            if self.numberValue >= self.maxValueInteger:
                self.error("Number out of limits")
            if self.input[self.tokenPos].isalpha():
                self.error("Number followed by a letter")
        else:
            self.tokenPos += 1
            if ch == '+':
                self.token = Symbol.PLUS
            elif ch == '-':
                self.token = Symbol.MINUS
            elif ch == '*':
                self.token = Symbol.MULT
            elif ch == '/':
                self.token = Symbol.DIV
            elif ch == '<':
                if self.input[self.tokenPos] == '=':
                    self.tokenPos += 1
                    self.token = Symbol.LE
                elif self.input[self.tokenPos] == '>':
                    self.tokenPos += 1
                    self.token = Symbol.NEQ
                else:
                    self.token = Symbol.LT
            elif ch == '>':
                if self.input[self.tokenPos] == '=':
                    self.tokenPos += 1
                    self.token = Symbol.GE
                else:
                    self.token = Symbol.GT
            elif ch == '=':
                if self.input[self.tokenPos] == '=':
                    self.tokenPos += 1
                    self.token = Symbol.EQ
                else:
                    self.token = Symbol.ASSIGN
            elif ch == '(':
                self.token = Symbol.LEFTPAR
            elif ch == ')':
                self.token = Symbol.RIGHTPAR
            elif ch == ',':
                self.token = Symbol.COMMA
            elif ch == ';':
                self.token = Symbol.SEMICOLON
            else:
                self.error('Invalid Character: "' + ch + '"')

    def error(self, message):
        if self.tokenPos == 0:
            self.tokenPos = 1
        else:
            if self.tokenPos >= len(self.input):
                self.tokenPos = len(self.input)

            strInput = self.input[self.tokenPos - 1:self.tokenPos]
            strError = 'Error at "' + strInput + '"'

            raise Exception(strError + " -> " + message)
