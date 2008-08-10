from AST import ast

class Expr(ast):
    def __init__(self, type):
        ast.__init__(self, type)

    def genC(self):
        raise NotImplementedError

    def eval(self):
        raise NotImplementedError
