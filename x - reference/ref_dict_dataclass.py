def print_hello():
    print(f"hello!!!!")


def print_goodbye():
    print(f"goodbye!!!!")


mydict = {
    "hello": print_hello,
    "goodbye": print_goodbye,
}


class MyClass:
    hello = print_hello
    goodbye = print_goodbye


# mydict["goodbye"]()
# mydict["hello"]()
# mydict["goodbye"]()
# mydict["goodbye"]()


print(f"****************************")

MyClass.hello()
