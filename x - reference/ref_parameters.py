fish_list = ["pike"]
fish_list_03 = ["shark"]


class FishyStuff:

    print(f"FISHY STUFF!!!!")

    print(f"{fish_list=}")

    def __init__(self, f_list: list[str]):
        self.f_list = f_list

    def fish_edit(self, wet_thing: list[str]):

        print(f"before******************")
        print(f"{fish_list=}")
        print(f"{wet_thing=}")

        wet_thing.append("cod")

        print(f"{fish_list=}")
        print(f"{wet_thing=}")

        self.f_list.append("clown")
        fish_list.append("goldfish")
        print(f"{wet_thing=}")

        return wet_thing


fs = FishyStuff(fish_list_03)


fish_list_02 = fs.fish_edit(fish_list)

print(f"{fish_list=}")
print(f"{fish_list_02=}")
print(f"{fs.f_list=}")
print(f"{fish_list_03=}")
