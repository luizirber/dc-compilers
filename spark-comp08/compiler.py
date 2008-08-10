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

    def t_keywords(self, s):
        r' var | begin | end | if | then | else | endif | read | write '
        self.rv.append(Token(type=s))

    def t_arithmetical_oper(self, s):
        r' \+ | - | \* | /'
        self.rv.append(Token(type=s))

    def t_logical_oper(self, s):
        r' <= | < | >= | > | == | <> '
        self.rv.append(Token(type=s))

    def t_number(self, s):
        r' \d+ '
        t = Token(type='number', attr=s)
        self.rv.append(t)

    def t_letter(self, s):
        r' [A-Za-z][A-Za-z]* '
        t = Token(type='letter', attr=s)
        self.rv.append(t)

    def t_punctuation(self, s):
        r' \( | \) | ; | , '
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
        GenericParser.__init__(self, start="Program")

    def p_program_1(self, args):
        " Program ::= var VarDecList ; CompositeStatement "
#        return Program(args[2], args[5])

    def p_program_2(self, args):
        " Program ::= CompositeStatement "
#        return Program(None, args[5])

    def p_vardeclist_1(self, args):
        ' VarDecList ::= Variable '
#        return args[0]

    def p_vardeclist_2(self, args):
        ' VarDecList ::= Variable , VarDecList ; '
#        arrayVariable = [args[0]]
#        if args[2]:
#            for decl in args[2]:
#                arrayVariable.append(decl)
#        return VarDecList(arrayVariable)

    def p_vardeclist_3(self, args):
        ' VarDecList ::= '
#        return None

    def p_compositestatement(self, args):
        " CompositeStatement ::= begin StatementList end "
#        return args[1]

    def p_statementlist_1(self, args):
        ' StatementList ::= '
#        return None

    def p_statementlist_2(self, args):
        ' StatementList ::= Statement ; StatementList '
#        arrayStatement = [args[0]]
#        if args[2]:
#            for statement in args[2]:
#                arrayStatement.append(statement)
#        return StatementList(arrayStatement)

    def p_statement_1(self, args):
        ' Statement ::= AssignmentStatement '
#        return args[0]

    def p_statement_2(self, args):
        ' Statement ::= IfStatement '
#        return args[0]

    def p_statement_3(self, args):
        ' Statement ::= ReadStatement '
#        return args[0]

    def p_statement_4(self, args):
        ' Statement ::= WriteStatement '
#        return args[0]

    def p_assignmentstatement(self, args):
        ' AssignmentStatament ::= Variable = Expr '
#        return AssignmentStatement

    def p_ifstatement_1(self, args):
        ' IfStatement ::= if Expr then StatementList'
#        return IfStatement(args[1], args[3], None)

    def p_ifstatement_2(self, args):
        ' IfStatement ::= if Expr then StatementList else StatementList'
#       return IfStatement(args[1], args[3], args[5])

    def p_readstatement(self, args):
        ' ReadStatement ::= read ( Variable ) '
#        return ReadStatement(args[2])

    def p_expr_1(self, args):
        ' expr ::= ( oper expr expr ) '
#        return CompositeExpr(args[2], args[1], args[3])

    def p_expr_2(self, args):
        ' expr ::= Number '
#        return NumberExpr(args[0].attr)

    def p_expr_3(self, args):
        ' expr ::= Variable '
#        name = str(args[0])
#        return VariableExpr(name, None)

    def p_variable(self, args):
        ' Variable ::= letter '
#        return Variable(str(args[0]))

    def p_oper_1(self, args):
        ' oper ::= - '
#        return str(args[0])

    def p_oper_2(self, args):
        ' oper ::= + '
#        return str(args[0])

    def p_oper_3(self, args):
        ' oper ::= * '
#        return str(args[0])

    def p_oper_4(self, args):
        ' oper ::= / '
#        return str(args[0])

    def p_oper_5(self, args):
        ' oper ::= < '
#        return str(args[0])

    def p_oper_6(self, args):
        ' oper ::= <= '
#        return str(args[0])

    def p_oper_7(self, args):
        ' oper ::= > '
#        return str(args[0])

    def p_oper_8(self, args):
        ' oper ::= >= '
#        return str(args[0])

    def p_oper_9(self, args):
        ' oper ::= == '
#        return str(args[0])

    def p_oper_10(self, args):
        ' oper ::= <> '
#        return str(args[0])

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

def scan(f):
    input = f.read()
    scanner = ProgramScanner()
    return scanner.tokenize(input)

def parse(tokens):
    parser = ProgramParser()
    return parser.parse(tokens)

def semantic(ast):
    DeclarationCheck(ast)
    return ast

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    f = open(filename)
    lexicon = scan(f)
    parse(lexicon)
#    program = semantic(ast)
#    program.genC()
    f.close()
