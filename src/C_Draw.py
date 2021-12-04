import pygame
import os

from pygame.constants import BLEND_RGBA_ADD, BLEND_RGB_ADD, BLEND_RGB_SUB


pygame.init()
pygame.display.set_caption("First Game")


def return_image(image, path, scale):
    res = pygame.image.load(os.path.join(path, image))
    res = pygame.transform.scale(res, scale)
    return res


imagesPath = 'res'


DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]

GRID_SIZE = 32
WIDTH, HEIGHT = (GRID_SIZE*2) + (GRID_SIZE *
                                 35), (GRID_SIZE*2) + (GRID_SIZE * 22)

win = pygame.Surface((WIDTH, HEIGHT))
WINDOW_SIZE = (WIDTH*1, HEIGHT*1)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)


COLOURS = {"BLACK": (0, 0, 0),
           "WHITE": (255, 255, 255),
           "BLACK_VERY_LIGHT": (210, 210, 210),
           "WHITE_4TH_4TH_4TH_4TH": (1, 1, 1),
           "RED": (255, 0, 0),
           "GREEN": (0, 255, 0),
           "BLUE_LIGHT": (125, 125, 255),
           "BLUE_VERY_LIGHT": (210, 210, 255)}

FONTS = {"monospace 50": pygame.font.SysFont("monospace", 15),
        "monospace 15": pygame.font.SysFont("monospace", 15)}

IMAGES = {"GRASS_IMAGE": return_image('grass.png', imagesPath, (GRID_SIZE, GRID_SIZE)),
          "DIRT_IMAGE": return_image('dirt.png', imagesPath, (GRID_SIZE, GRID_SIZE)),
          "ROCK_IMAGE": return_image('rock.png', imagesPath, (GRID_SIZE, GRID_SIZE))}


player_image = pygame.image.load(os.path.join(imagesPath, 'player_tran.png'))

player_image.set_colorkey((COLOURS["WHITE"]))
player_image = pygame.transform.scale(player_image, (player_image.get_width() * 2, player_image.get_height() * 2))


class Draw():
    def __init__(self, level):
        self.width = WIDTH
        self.height = HEIGHT
        self.grid_size = GRID_SIZE
        self.current_poistion = (0, 0)
        self.level = level

    def draw_lights(self, color, x, y):
        surface = pygame.Surface((self.grid_size, self.grid_size))
        pygame.draw.rect(surface, color, surface.get_rect())
        win.blit(surface, (x, y), special_flags=BLEND_RGB_ADD)

    def draw_outline(self, color, x, y):
        pygame.draw.rect(
            win, color, (x, y, self.grid_size - 1, self.grid_size - 1), 2)

    def draw_tile(self, image, x, y):
        win.blit(image, (x, y))

    def draw_tile_lights(self, image, x, y, rotate):
        image = pygame.transform.rotate(image, rotate)
        win.blit(image, (x, y), special_flags=BLEND_RGB_SUB)

    def draw(self, color, x, y):
        pygame.draw.rect(win, color, (x, y, self.grid_size, self.grid_size))

    def draw_transparent(self, color, x, y):
        surface = pygame.Surface((self.grid_size, self.grid_size))
        surface.set_alpha(75)
        pygame.draw.rect(surface, color, surface.get_rect())
        win.blit(surface, (x, y))

    def draw_circle(self, color, x, y):
        surface = pygame.Surface((self.grid_size, self.grid_size))
        pygame.draw.circle(win, color, (x, y), self.grid_size / 4)

    def draw_screen(self):
        surf = pygame.transform.scale(win, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()

    def draw_reset(self):
        win.fill(COLOURS["BLACK"])

    def draw_coordinates(self, words):
        self.font = FONTS["monospace 50"]
        words = str(words)
        text = self.font.render(words, 1, (COLOURS["RED"]))
        win.blit(text, (10, 10))

    def draw_debug_route(self, ai_contoller, run_debug):
        if run_debug == True:
            for p in ai_contoller.route_list:
                self.draw_outline(COLOURS["GREEN"], p[0], p[1])

    def draw_debug_ends(self, ai_contoller, run_debug):
        self.font = FONTS["monospace 15"]
        if run_debug == True:
            for k, v in dict.items(ai_contoller.path_type):
                text = self.font.render("{0}".format(v), 1, ((COLOURS["GREEN"])))
                win.blit(text, (k[0] + 1, k[1] + 5))

    def draw_light_positions(self, lights):
        for k, v in lights.light_positions.items():
            self.draw_lights(v, k[0], k[1])


    def draw_climb_positions_visited(self):
        for p in self.climb_positions_visited:
            if p not in self.water_list:
                pygame.draw.rect(
                    win, COLOURS["RED"], (p[0] + self.grid_size * 7/16, p[1], GRID_SIZE/8, GRID_SIZE))

    def draw_player(self):
        self.draw_tile(player_image, self.current_poistion[0] + ((GRID_SIZE - player_image.get_width())/2), self.current_poistion[1] + (GRID_SIZE - player_image.get_height()))


# FROM LEVEL


    def draw_paths(self):
        for p in self.level.paths:
            self.draw(COLOURS["WHITE_4TH_4TH_4TH_4TH"], p[0], p[1])

    def draw_level(self, rlp_tiles):
        for k, v in self.level.tiles.items():
            if v == 'S':
                self.draw((146, 244, 255), k[0], k[1])
            if v == 'G':
                self.draw_tile(IMAGES["GRASS_IMAGE"], k[0], k[1])
            if v == 'E':
                self.draw_tile(IMAGES["DIRT_IMAGE"], k[0], k[1])
            if v == 'P':
                self.draw_tile(IMAGES["ROCK_IMAGE"], k[0], k[1])
            if v == 'A':
                tile01 = pygame.image.load(rlp_tiles[k])
                tile01 = pygame.transform.scale(tile01, (GRID_SIZE, GRID_SIZE))
                self.draw_tile(tile01, k[0], k[1])

    def draw_water(self):
        for p in self.level.water_list:
            self.draw_transparent(COLOURS["BLUE_LIGHT"], p[0], p[1])

    def draw_build_grid(self, build_debug):
        if build_debug == True:
            for i in self.grid:
                # self.draw.draw_tile(dirt_image, i[0], i[1])
                self.draw(COLOURS["BLACK_VERY_LIGHT"], i[0], i[1])

    def draw_build_grid_hide(self, build_debug):
        if build_debug == True:
            directions_list = []
            for g in self.level.grid:
                for d in DIRECTIONS:
                    if (g[0] + (d[0] * GRID_SIZE), g[1] + (d[1] * GRID_SIZE)) not in self.level.wall_break_positions:
                        directions_list.append((d[0], d[1]))
                if len(directions_list) == 4:
                    self.draw_tile(IMAGES["DIRT_IMAGE"], g[0], g[1])
                directions_list.clear()

    def draw_build_wall_break_positions(self, build_debug):
        if build_debug == True:
            self.draw(COLOURS["BLACK_VERY_LIGHT"], self.level.wall_break_positions[-1][0], self.level.wall_break_positions[-1][1])
            pygame.display.update()
            pygame.time.delay(20)

    def draw_debug_climb_positions(self, run_debug):
        if run_debug == True:
            for p in self.level.climb_positions:
                pygame.draw.rect(win, COLOURS["GREEN"], (p[0] + GRID_SIZE * 7/16, p[1], GRID_SIZE/8, GRID_SIZE))

    def draw_debug_start_position(self, debug):
        if debug == True:
            p = self.level.past_positions[0]
            self.draw_outline(COLOURS["RED"], p[0], p[1])
