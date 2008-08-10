from AST import ast

class CompositeStatement(ast):
    def __init__(self, statement_list):
        ast.__init__(self, "CompositeStatement")
        self._kids = statement_list

    def genC(self):
        if self._kids:
            for statement in self._kids:
                statement.genC()
