from pprint import pprint
import inspect

# from dataclasses import dataclass


class Other:
    def catter(self):
        pass


class Test(Other):
    def fish(self):
        pass


# te = Test()

# pprint(inspect.getmembers(Test, inspect.isfunction))


# l = inspect.getclasstree(inspect.getmro(set))

# for i in l:
#     print(i)

# print("class")
pprint(dir(type))
