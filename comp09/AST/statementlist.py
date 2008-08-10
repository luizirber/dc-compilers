class StatementList(object):
    def __init__(self, v):
        self.v = v

    def genC(self):
        for statement in self.v:
            statement.genC()
