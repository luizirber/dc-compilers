from AST import ast

class VarDecList(ast):
    def __init__(self, arrayVariable):
        ast.__init__(self, "VarDecList")
        self._kids = arrayVariable

    def genC(self):
        if self._kids:
            for variable in self._kids:
                variable.genC()
