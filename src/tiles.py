# builtins
from os import path
from typing import Any

# packages
from PIL.Image import Image, open, composite, fromarray
from blend_modes import lighten_only
from numpy import ndarray, array, uint8

# local
from paths import Path_Data
from constants import IMAGE_TYPES, LIGHTING_TILE_ROTATE


files_for_image = {"rock_lighting_tile": "rock.png"}


images_path = "res"

# todo types to fix
T_array = Any

#! called by view > __init__ - 1 locaton
class Tile:
    def __init__(self, grid_size: int) -> None:

        # todo repeats - 4 variables
        self.rock_lighting_tile: Image = self.PIL_to_size_from_file(
            grid_size, images_path, "rock.png"
        )

        self.BlackSQ: Image = self.PIL_to_size_from_file(
            grid_size, images_path, "BlackSQ.png"
        )
        self.T_image: Image = self.PIL_to_size_from_file(
            grid_size, images_path, "I_Image_01.png"
        )
        self.TR_image: Image = self.PIL_to_size_from_file(
            grid_size, images_path, "Corner.png"
        )

    #! called by view > update - 1 location
    def update(
        self,
        surround_positions: dict[tuple[int, int], list[str]],
        width: int,
        top_offset: int,
        path_adjacent: list[tuple[int, int]],
        path_obj: Path_Data,
        grid_size: int,
        height: int,
    ):

        self.path_adjacent = path_adjacent
        self.paths = path_obj.paths

        self.create_tile_locations(width, height, top_offset, grid_size)

        tileImages = self.get_surround_images()

        self.route_light_positions_tiles = self.set_path_surround_tiles(
            tileImages,
            surround_positions,
            debug=False,
        )

        tiles = self.create_dict_tiles()

        return self.route_light_positions_tiles, tiles

    #! called by init - 4 location
    def PIL_to_size_from_file(
        self, grid_size: int, images_path: str, file_name: str
    ) -> Image:
        res_join = path.join(images_path, file_name)
        res_open = open(res_join)
        res_resize = res_open.resize((grid_size, grid_size))
        return res_resize

    #! called by update - 1 location
    def create_dict_tiles(self) -> dict[tuple[int, int], str]:
        TILE_LETTERS = [
            (self.rock, "R"),
            (self.path_adjacent, "A"),
            (self.sky, "S"),
            (self.grass, "G"),
            (self.paths, "P"),
        ]

        res_update: dict[tuple[int, int], str] = {}
        for i in TILE_LETTERS:
            res_fromkeys = dict.fromkeys(*i)
            res_update.update(res_fromkeys)

        return res_update

    #! called by update - 1 location
    def get_surround_images(self) -> dict[str, Image]:
        res_select_rotate: dict[str, Image] = {}

        for i in IMAGE_TYPES:
            res_select_rotate[i + "_image"] = self.select_rotate(
                self.T_image, self.TR_image, i
            )

        return res_select_rotate

    #! called by update - 1 location
    def create_tile_locations(
        self, width: int, height: int, top_offset: int, grid_size: int
    ) -> None:
        types = ["sky", "rock", "grass"]
        for t in types:
            self.create_tile_location(t, width, height, top_offset, grid_size)

    #! called by update - 1 location
    def set_path_surround_tiles(
        self,
        tileImages: dict[str, Image],
        path_surround_positions: dict[tuple[int, int], list[str]],
        debug: bool,
    ) -> dict[tuple[int, int], str]:

        # res_image: Image.Image = Image.Image()
        route_light_positions_tiles: dict[tuple[int, int], str] = {}

        for k, v in path_surround_positions.items():
            if len(v) == 1:
                res_image = self.select_rotate(self.T_image, self.TR_image, v[-1])
                res_image = res_image.convert("L")
                if not debug:
                    res_image = composite(
                        self.rock_lighting_tile, self.BlackSQ, res_image
                    )
                name: str = "Tiles\\" + str(k) + ".PNG"
                res_image.save(name)
                route_light_positions_tiles[k] = name
            elif len(v) == 2:
                res_image = self.image_darken(
                    tileImages[v[0] + "_image"], tileImages[v[1] + "_image"]
                )
                res_image = res_image.convert("L")
                if not debug:
                    res_image = composite(
                        self.rock_lighting_tile, self.BlackSQ, res_image
                    )
                name = "Tiles\\" + str(k) + ".PNG"
                res_image.save(name)
                route_light_positions_tiles[k] = name
            elif len(v) == 3:
                image01 = tileImages[v.pop() + "_image"]
                image02 = tileImages[v.pop() + "_image"]
                blend01 = self.image_darken(image01, image02)
                # blend01.show()
                image03 = tileImages[v.pop() + "_image"]
                blend02 = self.image_darken(blend01, image03)
                res_image = blend02
                res_image = res_image.convert("L")
                if not debug:
                    res_image = composite(
                        self.rock_lighting_tile, self.BlackSQ, res_image
                    )
                name = "Tiles\\" + str(k) + ".PNG"
                res_image.save(name)
                route_light_positions_tiles[k] = name

        return route_light_positions_tiles

    #! called by create_tile_location -  1 location
    def condition_y_start_stop(self, type, grid_size, top_offset, height):
        y_start: int = 0

        if type == "sky":
            y_start = 0
            y_stop = grid_size * top_offset - 1
        elif type == "rock":
            y_start = 0
            y_stop = height
        elif type == "grass":
            y_start = grid_size * (top_offset - 1)
            y_stop = grid_size * top_offset
        else:
            raise ValueError("Type not available")

        return (y_start, y_stop)

    #! called by create_tile_locations - 1 location
    def create_tile_location(
        self, type: str, width: int, height: int, top_offset: int, grid_size: int
    ) -> None:

        y_start_stop = self.condition_y_start_stop(type, grid_size, top_offset, height)

        res = [
            (x, y)
            for x in range(0, width, grid_size)
            for y in range(y_start_stop[0], y_start_stop[1], grid_size)
        ]

        exec(f"self.{type} = {res}")

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
        res = self.image_lighten(array_foreground, array_background, 1.0)
        return res

    #! called by image_darken - 2 location
    def tile_array(self, image: Image):
        res_array = array(image)
        res_array = res_array.astype(float)
        return res_array

    #! called by image_darken - 1 location
    def image_lighten(
        self, image_float01: Image, image_float02: Image, opacity: float
    ) -> Image:

        res_lighten_only = lighten_only(image_float01, image_float02, opacity)
        res_fromarrray = fromarray(uint8(res_lighten_only))
        return res_fromarrray
