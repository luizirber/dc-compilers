from AST import Statement

class ReadStatement(Statement):
    def __init__(self, v):
        self.v = v

    def genC(self):
        print '{ char s[256]; gets(s); sscanf(s, "%d", &' + self.v.getName() + "); }"
