from typing import Callable


def foo() -> Callable[[int, int], int]:
    func: Callable[[int, int], int] = lambda x, y: x + (y*2)
    return func


l = foo()
print(l(1, 2))
