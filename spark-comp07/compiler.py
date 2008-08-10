#
#  comp7
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

from spark import GenericScanner, GenericParser, GenericASTTraversal

from token import Token

from AST import (CompositeExpr, NumberExpr, Program, Variable,
                 VariableExpr, VarDecList)

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

    symbolTable = {}

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
        return VarDecList(arrayVariable)

    def p_vardeclist_2(self, args):
        ' vardeclist ::= '
        return None

    def p_vardec(self, args):
        ' vardec ::= letter = number '
        name = str(args[0])
        return Variable(name, args[2].attr)

    def p_expr_1(self, args):
        ' expr ::= ( oper expr expr ) '
        return CompositeExpr(args[2], args[1], args[3])

    def p_expr_2(self, args):
        ' expr ::= number '
        return NumberExpr(args[0].attr)

    def p_expr_3(self, args):
        ' expr ::= letter '
        name = str(args[0])
        return VariableExpr(name, None)

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

class DeclarationCheck(GenericASTTraversal):
    def __init__(self, ast):
        GenericASTTraversal.__init__(self, ast)
        self.symbolTable = {}
        self.preorder()

    def n_Variable(self, node):
        name = node.name
        try:
            self.symbolTable[name]
        except KeyError:
            self.symbolTable[name] = int(node.value)
        else:
            print 'Variable', name, 'has already been declared'
            sys.exit(1)
            #TODO: definir funcao error

    def n_VariableExpr(self, node):
        name = node.name
        try:
            e = self.symbolTable[name]
        except KeyError:
            print 'Variable', name,'was not declared'
            sys.exit(1)
            #TODO: implementar erro
        else:
            node.value = e

class Interpret(GenericASTTraversal):
    def __init__(self, ast):
        GenericASTTraversal.__init__(self, ast)
        self.postorder()
        print ast.value

    def n_Program(self, node):
        node.value = node[1].value

    def n_CompositeExpr(self, node):
        evalLeft = node[0].value
        evalRight = node[1].value

        if node.attr == '+':
            node.value = evalLeft + evalRight
        elif node.attr == '-':
            node.value = evalLeft - evalRight
        elif node.attr == '*':
            node.value = evalLeft * evalRight
        elif node.attr == '/':
            if evalRight == 0:
                print "Division by zero"
                sys.exit(1)
            node.value = evalLeft + evalRight
        else:
            print "Unknown operator"
            sys.exit(1)

def scan(f):
    input = f.read()
    scanner = ProgramScanner()
    return scanner.tokenize(input)

def parse(tokens):
    parser = ProgramParser()
    return parser.parse(tokens)

def semantic(ast):
    DeclarationCheck(ast)
    Interpret(ast)
    return ast

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    f = open(filename)
    lexicon = scan(f)
    ast = parse(lexicon)
    program = semantic(ast)
    f.close()
