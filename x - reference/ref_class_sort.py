class Foo(object):
    def __init__(self, score):
        self.score = score

    def __repr__(self) -> str:
        return f"foo: {self.score=}"

    def __lt__(self, other):
        return self.score < other.score

    def __ge__(self, other):
        return self.score >= other.score


l = [Foo(3), Foo(1), Foo(2)]

# l.sort(reverse=True)

# print(f"{l=}")


print(l[0] <= l[1])
