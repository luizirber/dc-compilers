from AST import ast

class Statement(ast):
    def __init__(self, type):
        ast.__init__(self, type)

    def genC(self):
        raise NotImplementedError
