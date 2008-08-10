#
#  comp5
#  This program is a synthatic analyzer and evaluator for the
#  following grammar:
#
#  Expr ::= '(' oper Expr Expr ')' | number
#  oper ::= '+' | '-'
#  number ::= '0' | '1' | ... | '9'
#
#  The evaluation of the expression is printed in the standard output

import sys

from spark import GenericScanner, GenericParser

from token import Token

from AST import CompositeExpr, NumberExpr

class ExprScanner(GenericScanner):
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
        r' \+ | - '
        self.rv.append(Token(type=s))

    def t_number(self, s):
        r' [0-9] '
        t = Token(type='number', attr=s)
        self.rv.append(t)

    def t_parens(self, s):
        r' \( | \) '
        self.rv.append(Token(type=s))

    def t_eof(self, s):
        r' \\0 '
        self.rv.append(Token(type=s))

class ExprParser(GenericParser):
    def __init__(self):
        GenericParser.__init__(self, start="expr")

    def p_expr_1(self, args):
        ' expr ::= ( oper expr expr ) '
        return CompositeExpr(args[2], args[1], args[3])

    def p_expr_2(self, args):
        ' expr ::= number '
        return NumberExpr(args[0].attr)

    def p_expr_3(self, args):
        ' expr ::= letter '
        return str(args[0])

    def p_oper_1(self, args):
        ' oper ::= - '
        return str(args[0])

    def p_oper_2(self, args):
        ' oper ::= + '
        return str(args[0])

def scan(f):
    input = f.read()
    scanner = ExprScanner()
    return scanner.tokenize(input)

def parse(tokens):
    parser = ExprParser()
    return parser.parse(tokens)

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    f = open(filename)
    e = parse(scan(f))
    e.genC()
    f.close()
