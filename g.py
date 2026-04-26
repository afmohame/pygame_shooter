class t():
    def __init__(self):
        self.a = 2
    def m(self):
        self.b = 3

g = t()
print(g.a)
f = g.m()
print(g.b)