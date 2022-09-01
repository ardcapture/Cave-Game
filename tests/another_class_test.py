class class01:
    field01 = "yes_filed01!"

    def __init__(self, filed03) -> None:
        self.field02 = "yes_filed02!"
        self.field03 = filed03

    def class01_print01(field01):
        print(f"print01: {field01}")

    def class01_print01_v02(field01):
        print(f"print01: {field01}")

    def class01_print02(self):
        print(f"print02: {self.field02}")

    def class01_print02_v02(self, field02):
        print(f"print02: {field02}")

    def class01_print03(self):
        print(f"print02: {self.field03}")


def main():
    print(f"class test start!")
    print(f"{class01.field01=}")

    myfield = class01.field01
    class01.class01_print01(myfield)

    obj01 = class01("yes_filed03!")
    obj02 = class01("yes_filed03!")

    class01.class01_print02(obj01)

    class01.class01_print03(obj01)

    obj02.field04 = "yes field04 another"

    class01.field04 = "yes field04"

    print(f"{class01.field04=}")
    print(f"{obj01.field04=}")
    print(f"{obj02.field04=}")

    obj01.class01_print01_v02()


if __name__ == "__main__":
    main()
