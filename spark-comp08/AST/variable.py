from AST import ast

class Variable(ast):
    def __init__(self, name):
        ast.__init__(self, "Variable")
        self.name = name

    def genC(self):
        print "int", self.name, ';'
