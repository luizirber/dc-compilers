from AST import ast

class StatementList(ast):
    def __init__(self, v):
        ast.__init__(self, "StatementList")
        self._kids = [v]

    def genC(self):
        for statement in self._kids[0]:
            statement.genC()
