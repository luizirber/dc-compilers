from AST import ast

class Variable(ast):
    def __init__(self, name, value):
        ast.__init__(self, "Variable")
        self.name = name
        self.value = value

    def genC(self):
        print "int", self.name, '=', self.value, ';'
