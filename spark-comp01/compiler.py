#
#  comp1
#  This program is a synthatic analyzer for the following grammar:
#
#  Expr ::= '(' oper Expr Expr ')' | number
#  oper ::= '+' | '-'
#  number ::= '0' | '1' | ... | '9'
#
#  Example of program:
#
#  (+ (-5 4) 2)

from spark import GenericScanner, GenericParser

from token import Token

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

    def t_oper(self, s):
        r' \+ | -'
        self.rv.append(Token(type=s))

    def t_number(self, s):
        r' [0-9] '
        t = Token(type='number', attr=s)
        self.rv.append(t)

    def t_parens(self, s):
        r' \( | \) '
        self.rv.append(Token(type=s))

class ExprParser(GenericParser):
    def __init__(self):
        GenericParser.__init__(self, start="expr")

    def p_expr_1(self, args):
        ' expr ::= ( oper expr expr ) '

    def p_expr_2(self, args):
        ' expr ::= number '

    def p_oper_1(self, args):
        ' oper ::= - '

    def p_oper_2(self, args):
        ' oper ::= + '

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
    parse(scan(f))
    f.close()
