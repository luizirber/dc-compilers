from AST import Statement

class ReadStatement(Statement):
    def __init__(self, v):
        Statement.__init__(self, "ReadStatement")
        self._kids.append(v)

    def genC(self):
        print ('{ char s[256]; gets(s); sscanf(s, "%d", &'
                + self._kids[0].getName() + "); }")
