#
#  comp3
#  This program is a synthatic analyzer and code generator for the
#  following grammar:
#
#  Expr ::= '(' oper Expr Expr ')' | number
#  oper ::= '+' | '-'
#  number ::= '0' | '1' | ... | '9'
#
#  The code is generated to ASM as described in Chapter 8 of the primer
#  'Construcao de Compiladores'. The generated code is as bad as anyone can ever
#  design, but it is enough to show how assembler code is produced.

import sys

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
        result = []
        result.append(str(args[2]))
        result.append(str(args[3]))
        result.append('pop  R1\n')
        result.append('pop  R0\n')
        if args[1].type == '+':
            result.append('add  R0, R1\n')
        elif args[1].type == '-':
            result.append('sub  R0, R1\n')
        result.append('push R0\n')
        return ''.join(result)

    def p_expr_2(self, args):
        ' expr ::= number '
        return ('mov  R0, ' + str(args[0]) + '\npush R0\n')

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
