# my_int = 5


# def change_parmarmeter(parm_int):

#     print(f"before: {parm_int=}")

#     parm_int += 5

#     print(f"after: {parm_int=}")

#     return parm_int


# print(f"before: {my_int=}")

# func_int = change_parmarmeter(my_int)

# print(f"after: {my_int=}")

# print(f"{func_int=}")


# my_bool = func_int is my_int

# print(f"{my_bool=}")


# x = "global test"


# def make_list():
#     global x
#     x = "local test"
#     print(f"{x=}")

#     # global my_list
#     # my_list = ["one item"]


# # print(f"{my_list=}")

# make_list()

# print(f"{x=}")


#!!! **************

# x = "global x"


# def outer():
#     # global x
#     x = "outer x"

#     def inner():
#         # nonlocal x
#         x = "inner x"
#         print(x)

#     inner()
#     print(x)


# outer()

# print(x)


#!!! **************


# my_list = ["one item"]


# def change_list(a_list: list):
#     a_list.append(a_list)
#     # a_list = ["different items"] + a_list
#     return a_list


# my_list_02 = change_list(my_list)

# print(my_list)
# print(my_list_02)

# my_bool = my_list is my_list_02


# print(f"{my_list=}")

# for i in my_list:
#     for ii in i:
#         print(f"{i=}")
#         print(f"{ii=}")

# my_bool_02 = my_list_02[-1] is my_list

# print(f"{my_bool_02=}")


# print(my_bool)

#! **************


# my_set = {1, 3, 56, 7, 8}

# print(my_set)


# def set_stuff(a_set: set):
#     a_set.add(11)


# set_stuff(my_set)

# print(my_set)


#! **************


# my_int = 5


# def int_stuff(a_int: int):
#     my_bool = my_int is a_int

#     print(f"{my_bool=}")

#     return a_int


# my_int_02 = int_stuff(my_int)

# my_bool = my_int is my_int_02

# print(f"{my_bool=}")


import random


class MakeStuff:
    def __init__(self):
        self.x = [1, 2, 4]
        self.make_s_list = self.make_list()

    def make_list(self):
        num = random.randint(3, 99)
        self.x.append(num)
        print(f"{id(self.x)=}")
        print(f"{self.x=}")

        return self.x


class MoreStuff:
    def __init__(self, a_list: list[int]):
        self.a_list = a_list

    def append_list(self, number: int):

        self.a_list.append(number)
        print(f"{id(self.a_list)=}")
        print(f"{self.a_list=}")


makestuff = MakeStuff()

my_x = makestuff.make_s_list

print(f"**{id(my_x)=}")
print(f"**{my_x=}")

makestuff.make_list()

print(f"**{id(my_x)=}")
print(f"**{my_x=}")

morestuff = MoreStuff(my_x)

morestuff.append_list(300)

print(f"**{id(my_x)=}")
print(f"**{my_x=}")


morestuff.append_list(300)

print(f"**{id(my_x)=}")
print(f"**{my_x=}")


print(f"{id(makestuff.x)=}")
print(f"{makestuff.x=}")
