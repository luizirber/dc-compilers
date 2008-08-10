class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def genC(self):
        print "int", self.name, '=', self.value, ';'
