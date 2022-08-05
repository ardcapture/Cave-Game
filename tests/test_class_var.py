
# print(f"{vars(Foo())}")
# print(f"{vars(Foo()).keys()}")


class Foo(object):
    def __init__(self):
        self.a = 1
        self.b = 2

    def func(self):
        pass


class hi:
    def __init__(self):
        self.ii = "foo"
        self.kk = "bar"


hi_obj = hi()
foo_obj = Foo()

print(f"hi_obj: {hi_obj.__dict__.keys()}")
print(f"foo_obj: {foo_obj.__dict__.keys()}")
