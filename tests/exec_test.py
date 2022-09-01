from dataclasses import dataclass
from typing import NamedTuple


mydict = {
    "rock_lighting_tile": "'rock.png'",
}


def files_to_images(dictionary):
    images = {}
    for k, v in dictionary.items():
        print(f"{k=}{v=}")
        images[k] = v
        # exec(f"{images[k]} = {v}")
    return images


images = files_to_images(mydict)


hello = "'hello'"


word = "rock_lighting_tile"

print(f"images: {images}")

print(f"hello: {hello}")


for k in range(5):
    exec(f"cat_{k} = k*2")


print(cat_0)
print(cat_1)
print(cat_2)
