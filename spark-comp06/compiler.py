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

from spark import GenericScanner, GenericParser

from token import Token

from AST import CompositeExpr, NumberExpr, Program, Variable, VariableExpr

class ProgramScanner(GenericScanner):
    def __init__(self):
        GenericScanner.__init__(self)

    def tokenize(self, input):
        self.rv = []
        GenericScanner.tokenize(self, input)
        return self.rv

    def t_whitespace(self, s):
        r' \s+ '
        pass

    def t_escape(self, s):
        r' [\t\r\n]'
        pass

    def t_oper(self, s):
        r' \+ | - | \* | /'
        self.rv.append(Token(type=s))

    def t_number(self, s):
        r' [0-9] '
        t = Token(type='number', attr=s)
        self.rv.append(t)

    def t_letter(self, s):
        r' [A-Za-z] '
        t = Token(type='letter', attr=s)
        self.rv.append(t)

    def t_parens(self, s):
        r' \( | \) '
        self.rv.append(Token(type=s))

    def t_colon(self, s):
        r' : '
        self.rv.append(Token(type=s))

    def t_assign(self, s):
        r' = '
        self.rv.append(Token(type=s))

    def t_eof(self, s):
        r' \\0 '
        self.rv.append(Token(type=s))

class ProgramParser(GenericParser):
    def __init__(self):
        GenericParser.__init__(self, start="program")

    def p_program(self, args):
        ' program ::= vardeclist : expr '
        return Program(args[0], args[2])

    def p_vardeclist_1(self, args):
        ' vardeclist ::= vardec vardeclist'
        arrayVariable = [args[0]]
        if args[1]:
            for decl in args[1]:
                arrayVariable.append(decl)
        return arrayVariable

    def p_vardeclist_2(self, args):
        ' vardeclist ::= '
        return None

    def p_vardec(self, args):
        ' vardec ::= letter = number '
        return Variable(args[0], args[2])

    def p_expr_1(self, args):
        ' expr ::= ( oper expr expr ) '
        return CompositeExpr(args[2], args[1], args[3])

    def p_expr_2(self, args):
        ' expr ::= number '
        return NumberExpr(args[0].attr)

    def p_expr_3(self, args):
        ' expr ::= letter '
        return VariableExpr(str(args[0]))

    def p_oper_1(self, args):
        ' oper ::= - '
        return str(args[0])

    def p_oper_2(self, args):
        ' oper ::= + '
        return str(args[0])

    def p_oper_3(self, args):
        ' oper ::= * '
        return str(args[0])

    def p_oper_4(self, args):
        ' oper ::= / '
        return str(args[0])

def scan(f):
    input = f.read()
    scanner = ProgramScanner()
    return scanner.tokenize(input)

def parse(tokens):
    parser = ProgramParser()
    return parser.parse(tokens)

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    f = open(filename)
    e = parse(scan(f))
    e.genC()
    f.close()
