import os
from typing import TYPE_CHECKING

# from dataclasses import dataclass
import blend_modes as bm
import numpy
from PIL import Image as PIL_Image
from PIL.Image import Image


from src.utilities import IMAGE_TYPES, LIGHTING_TILE_ROTATE
from src.position import Position

if TYPE_CHECKING:
    from src.level import Level
    from src.View import View


#! called by view > __init__ - 1 location
class Tile:
    images_path = "res"

    def __init__(self, level: "Level") -> None:
        self.grid_size = level.GRID_SIZE

        self.path_surround_tiles_debug = False

        # todo repeats - 4 variables
        self.rock_lighting_tile: Image = self.PIL_to_size_from_file(
            self.grid_size, self.images_path, "rock.png"
        )

        self.BlackSQ: Image = self.PIL_to_size_from_file(
            self.grid_size, self.images_path, "BlackSQ.png"
        )
        self.T_image: Image = self.PIL_to_size_from_file(
            self.grid_size, self.images_path, "I_Image_01.png"
        )
        self.TR_image: Image = self.PIL_to_size_from_file(
            self.grid_size, self.images_path, "Corner.png"
        )

    #! called by init - 4 location
    def PIL_to_size_from_file(
        self, grid_size: int, images_path: str, file_name: str
    ) -> Image:
        res_join = os.path.join(images_path, file_name)
        res_open = PIL_Image.open(res_join)
        return res_open.resize((grid_size, grid_size))

    @property
    def tileImages(self) -> dict[str, Image]:
        return {
            f"{i}_image": self.select_rotate(self.T_image, self.TR_image, i)
            for i in IMAGE_TYPES
        }

    #! called by update - 1 location
    def set_path_surround_tiles(self, view: "View", level: "Level"):
        # res_image: Image.Image = Image.Image()
        route_light_positions_tiles: dict[Position, str] = {}

        for k, v in view.surround.surround_positions(level).items():
            if len(v) == 1:
                res_image = self.select_rotate(self.T_image, self.TR_image, v[-1])
                res_image = res_image.convert("L")
                if not self.path_surround_tiles_debug:
                    res_image = PIL_Image.composite(
                        self.rock_lighting_tile, self.BlackSQ, res_image
                    )
                name: str = "Tiles\\" + str(k) + ".PNG"
                res_image.save(name)
                route_light_positions_tiles[k] = name
            elif len(v) == 2:
                res_image = self.image_darken(
                    self.tileImages[f"{v[0]}_image"], self.tileImages[f"{v[1]}_image"]
                )

                res_image = res_image.convert("L")
                if not self.path_surround_tiles_debug:
                    res_image = PIL_Image.composite(
                        self.rock_lighting_tile, self.BlackSQ, res_image
                    )
                name = "Tiles\\" + str(k) + ".PNG"
                res_image.save(name)
                route_light_positions_tiles[k] = name
            elif len(v) == 3:
                image01 = self.tileImages[f"{v.pop()}_image"]
                image02 = self.tileImages[f"{v.pop()}_image"]
                blend01 = self.image_darken(image01, image02)
                # blend01.show()
                image03 = self.tileImages[f"{v.pop()}_image"]
                blend02 = self.image_darken(blend01, image03)
                res_image = blend02
                res_image = res_image.convert("L")
                if not self.path_surround_tiles_debug:
                    res_image = PIL_Image.composite(
                        self.rock_lighting_tile, self.BlackSQ, res_image
                    )
                name = "Tiles\\" + str(k) + ".PNG"
                res_image.save(name)
                route_light_positions_tiles[k] = name

        return route_light_positions_tiles

    #! called by get_surround_images - 1 location
    #! called bt set_path_surround_tiles - 1 location
    def select_rotate(
        self, TOP_image: Image, TOP_R_image: Image, neighbor: str
    ) -> Image:
        image: Image

        if LIGHTING_TILE_ROTATE[neighbor][0] == "TOP_image":
            image = TOP_image
        elif LIGHTING_TILE_ROTATE[neighbor][0] == "TOP_R_image":
            image = TOP_R_image

        return image.rotate(LIGHTING_TILE_ROTATE[neighbor][1])

    #! called by set_path_surround_tiles - 3 location
    def image_darken(self, foreground_image: Image, background_image: Image) -> Image:
        array_foreground = self.tile_array(foreground_image)
        array_background = self.tile_array(background_image)
        return self.image_lighten(array_foreground, array_background, 1.0)

    #! called by image_darken - 2 location
    def tile_array(self, image: Image):
        res_array = numpy.array(image)
        return res_array.astype(float)

    #! called by image_darken - 1 location
    def image_lighten(
        self, image_float01: Image, image_float02: Image, opacity: float
    ) -> Image:
        res_lighten_only = bm.lighten_only(image_float01, image_float02, opacity)
        return PIL_Image.fromarray(numpy.uint8(res_lighten_only))
