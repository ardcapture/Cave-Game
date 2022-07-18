import pygame
import os



from pygame.constants import BLEND_RGBA_ADD, BLEND_RGB_ADD, BLEND_RGB_SUB

from C_Model import Game_OLD


IMAGESPATH = 'res'


DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]


COLOURS = {"BLACK": (0, 0, 0),
           "WHITE": (255, 255, 255),
           "BLACK_VERY_LIGHT": (210, 210, 210),
           "WHITE_4TH_4TH_4TH_4TH": (1, 1, 1),
           "RED": (255, 0, 0),
           "GREEN": (0, 255, 0),
           "BLUE_LIGHT": (125, 125, 255),
           "BLUE_VERY_LIGHT": (210, 210, 255)}


class View():
    def __init__(self, title: str, width: int, height: int):
        # def __init__(self, title: str, width: int, height: int, timestep: int = 50):

        self.grid_size = 32
        self.width = (self.grid_size * 2) + (self.grid_size * width)
        self.height = (self.grid_size*2) + (self.grid_size * height)

        self.window_size = (self.width*1, self.height*1)

        pygame.init()
        pygame.display.set_caption(title)
        self.win = pygame.display.set_mode(size=(self.width * 1, self.height * 1), flags=0, depth=32)

        self.surface = pygame.Surface((self.width, self.height))

        self.current_position = (0, 0)

        self.initialize()

    def initialize(self):
        self.set_player_image()
        self.set_images()
        self.set_fonts()

    def run(self, game_map: Game_OLD, run_debug_state: bool, controller):

        self.draw_level(game_map)
        self.draw_coordinates(controller.mousePos)

        self.draw_player()
        self.draw_water(game_map)
        self.draw_light_positions(game_map)
        self.draw_debug_start_position(game_map, run_debug_state)
        self.draw_debug_climb_positions(game_map, run_debug_state)
        self.draw_debug_ends(game_map, run_debug_state)
        self.draw_debug_route(game_map, run_debug_state)
        self.draw_screen()

    def set_images(self):
        self.images = {"GRASS_IMAGE": self.return_image('grass.png', IMAGESPATH, (self.grid_size, self.grid_size)),
                       "DIRT_IMAGE": self.return_image('dirt.png', IMAGESPATH, (self.grid_size, self.grid_size)),
                       "ROCK_IMAGE": self.return_image('rock.png', IMAGESPATH, (self.grid_size, self.grid_size))}

    def set_fonts(self):
        self.fonts = {"monospace 50": pygame.font.SysFont("monospace", 15),
                      "monospace 15": pygame.font.SysFont("monospace", 15)}

    def return_image(self, image, path, scale):
        res = pygame.image.load(os.path.join(path, image))
        res = pygame.transform.scale(res, scale)
        return res

    def set_player_image(self):
        player_image = pygame.image.load(os.path.join(IMAGESPATH, 'player_tran.png'))

        player_image.set_colorkey((COLOURS["WHITE"]))
        self.player_image = pygame.transform.scale(player_image, (player_image.get_width() * 2, player_image.get_height() * 2))

    def draw_lights(self, color, x, y):
        surface = pygame.Surface((self.grid_size, self.grid_size))
        pygame.draw.rect(surface, color, surface.get_rect())
        self.surface.blit(surface, (x, y), special_flags=BLEND_RGB_ADD)

    def draw_outline(self, color, x, y):
        pygame.draw.rect(
            self.surface, color, (x, y, self.grid_size - 1, self.grid_size - 1), 2)

    def draw_tile(self, image, x, y):
        self.surface.blit(image, (x, y))

    def draw_tile_lights(self, image, x, y, rotate):
        image = pygame.transform.rotate(image, rotate)
        self.surface.blit(image, (x, y), special_flags=BLEND_RGB_SUB)

    def draw(self, color, x, y):
        # surface = pygame.Surface((self.grid_size, self.grid_size)) #TODO ?
        pygame.draw.rect(self.surface, color, (x, y, self.grid_size, self.grid_size))
        # self.win.blit(surface, (x, y)) # TODO ?!

    def draw_v02(self, model):
        for obj in model.objs:
            # self.draw(obj.material, obj.position[0], obj.position[1])
            pygame.draw.rect(self.surface, obj.material, (obj.position[0], obj.position[1], self.grid_size, self.grid_size))

        surf = pygame.transform.scale(self.surface, self.window_size)
        self.win.blit(surf, (0, 0))
        pygame.display.update()
        # pygame.time.delay(40)

        # surface = pygame.Surface((self.grid_size, self.grid_size)) #TODO ?
        # pygame.draw.rect(win, color, (x, y, self.grid_size, self.grid_size))
        # win.blit(surface, (x, y)) # TODO ?!

    def draw_transparent(self, color, x, y):
        surface = pygame.Surface((self.grid_size, self.grid_size))
        surface.set_alpha(75)
        pygame.draw.rect(surface, color, surface.get_rect())
        self.surface.blit(surface, (x, y))

    def draw_circle(self, color, x, y):
        surface = pygame.Surface((self.grid_size, self.grid_size))
        pygame.draw.circle(self.surface, color, (x, y), self.grid_size / 4)

    def draw_screen(self):
        surf = pygame.transform.scale(self.surface, self.window_size)
        self.win.blit(surf, (0, 0))
        pygame.display.update()

    def draw_reset(self):
        self.surface.fill(COLOURS["BLACK"])

    def draw_coordinates(self, words):
        self.font = self.fonts["monospace 50"]
        words = str(words)
        text = self.font.render(words, 1, (COLOURS["RED"]))
        self.surface.blit(text, (10, 10))

    def draw_debug_route(self, level, run_debug):
        if run_debug:
            for p in level.list_route:
                self.draw_outline(COLOURS["GREEN"], p[0], p[1])

    def draw_debug_ends(self, level, run_debug):
        if not run_debug:
            return

        self.font = self.fonts["monospace 15"]
        for k, v in dict.items(level.dict_path_type):
            text = self.font.render("{0}".format(v), 1, ((COLOURS["GREEN"])))
            self.surface.blit(text, (k[0] + 1, k[1] + 5))

    def draw_light_positions(self, model):
        for k, v in model.light_positions.items():
            self.draw_lights(v, k[0], k[1])

    def draw_climb_positions_visited(self):
        for p in self.climb_positions_visited:
            if p not in self.water_list:
                pygame.draw.rect(self.surface, COLOURS["RED"], (p[0] + self.grid_size * 7/16, p[1], self.grid_size/8, self.grid_size))

    def draw_player(self):
        self.draw_tile(self.player_image, self.current_position[0] + ((self.grid_size - self.player_image.get_width())/2), self.current_position[1] + (self.grid_size - self.player_image.get_height()))


# FROM LEVEL

    # def draw_paths(self):
    #     for p in self.level.paths:
    #         self.draw(COLOURS["WHITE_4TH_4TH_4TH_4TH"], p[0], p[1]) # TODO check if being used

    def draw_level(self, model):
        for k, v in model.tiles.items():
            if v == 'S':
                self.draw((146, 244, 255), k[0], k[1])
            if v == 'G':
                self.draw_tile(self.images["GRASS_IMAGE"], k[0], k[1])
            if v == 'E':
                self.draw_tile(self.images["DIRT_IMAGE"], k[0], k[1])
            if v == 'P':
                self.draw_tile(self.images["ROCK_IMAGE"], k[0], k[1])
            # if v == 'A':
            #     # tile01 = pygame.image.load(model.route_light_positions_tiles[k])
            #     tile01 = pygame.transform.scale(tile01, (self.grid_size, self.grid_size))
            #     self.draw_tile(tile01, k[0], k[1])

    def draw_water(self, model):
        for p in model.list_water_list:
            self.draw_transparent(COLOURS["BLUE_LIGHT"], p[0], p[1])

    def draw_build_grid(self, model):
        for i in model.grid:
            self.draw(COLOURS["BLACK_VERY_LIGHT"], i[0], i[1])

    def draw_build_grid_hide(self, model, build_debug):
        if build_debug:
            directions_list = []
            for g in model.list_grid:
                for d in DIRECTIONS:
                    if (g[0] + (d[0] * self.grid_size), g[1] + (d[1] * self.grid_size)) not in model.list_wall_break_positions:
                        directions_list.append((d[0], d[1]))
                if len(directions_list) == 4:
                    self.draw_tile(self.images["DIRT_IMAGE"], g[0], g[1])
                directions_list.clear()

    def draw_build_wall_break_positions(self, level, build_debug):
        level02 = level
        if build_debug:
            self.draw(COLOURS["BLACK_VERY_LIGHT"], level02.list_wall_break_positions[-1][0], level02.list_wall_break_positions[-1][1])
            pygame.display.update()
            pygame.time.delay(20)

    def draw_debug_climb_positions(self, model, run_debug):
        if run_debug:
            for p in model.list_climb_positions:
                pygame.draw.rect(self.surface, COLOURS["GREEN"], (p[0] + self.grid_size * 7/16, p[1], self.grid_size/8, self.grid_size))

    def draw_debug_start_position(self, model, debug):
        if debug:
            p = model.list_past_positions[0]
            self.draw_outline(COLOURS["RED"], p[0], p[1])
