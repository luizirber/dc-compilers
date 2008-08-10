#
#  comp4
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

class CompSyntaxError(Exception):
    def __init__(self, lineno, token=None, msg=None):
        self.lineno = lineno
        self.token = token
        self.msg = msg

    def __str__(self):
        if self.msg is None:
            return "Error at '%s', line %d" % (self.token, self.lineno)
        else:
            return "%s, line %d" % (self.msg, self.lineno)

class ExprScanner(GenericScanner):
    def __init__(self):
        GenericScanner.__init__(self)
        self.lineno = 1

    def tokenize(self, input):
        self.rv = []
        GenericScanner.tokenize(self, input)
        return self.rv

    def t_whitespace(self, s):
        r' \s+ '
        pass

    def t_tab(self, s):
        r' \t'
        pass

    def t_newline(self, s):
        r' \n'
        self.lineno += 1

    def t_oper(self, s):
        r' \+ | -'
        self.rv.append(Token(type=s, lineno=self.lineno))

    def t_number(self, s):
        r' [0-9] '
        t = Token(type='number', attr=s, lineno=self.lineno)
        self.rv.append(t)

    def t_parens(self, s):
        r' \( | \) '
        self.rv.append(Token(type=s, lineno=self.lineno))

    def t_eof(self, s):
        r' \\0 '
        self.rv.append(Token(type=s, lineno=self.lineno))

class ExprParser(GenericParser):
    def __init__(self):
        GenericParser.__init__(self, start="expr")

    def error(self, tok):
        raise CompSyntaxError(tok.lineno, tok)

    def p_expr_1(self, args):
        ' expr ::= ( oper expr expr ) '
        if args[1] == '+':
            return args[2] + args[3]
        elif args[1] == '-':
            return args[2] - args[3]

    def p_expr_2(self, args):
        ' expr ::= number '
        return int(args[0].attr)

    def p_oper_1(self, args):
        ' oper ::= - '
        return args[0]

    def p_oper_2(self, args):
        ' oper ::= + '
        return args[0]

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
    print parse(scan(f))
    f.close()
