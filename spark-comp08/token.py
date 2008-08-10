class Token(object):
    def __init__(self, type, attr=None):
        self.type = type
        self.attr = attr

    def __cmp__(self, o):
        return cmp(self.type, o)

    def __repr__(self):
        return self.attr or self.type
