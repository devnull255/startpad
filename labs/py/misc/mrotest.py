class Foo(object):
    def f(self):
        print "Foo"

class Bar(object):
    def f(self):
        print "Bar"
        super(Bar, self).f()

class Bazz(Bar, Foo):
    def f(self):
        print "Bazz"
        super(Bazz, self).f()

x = Bazz()
x.f()

