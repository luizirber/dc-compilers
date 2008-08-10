class Variable:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def genC(self):
        print "int", self.name + ';'
