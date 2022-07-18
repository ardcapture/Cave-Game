import sys
import keyboard
import mouse


import pygame
import random

import C_Model
import D_View


GRID_SIZE = 32


DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]


LevelStates = ["01_Title", "02_Settings", "03_Build", "04_Play"]
game_keys = "K_BACKQUOTE"
run_debug_state = False
lights_state = False
build_debug = False


# TODO may not get used!
state = {
    # "title": title,
    # "level_build": build,
    # "level_run": level_run,
    # "level_pause": level_pause
}


class Game_NEW:
    def __init__(self):

        self.clock = pygame.time.Clock()

    # TODO Game methods **************************:

    # TODO initalize (instantiate game's class, and there instances)
    def initialize(self):
        self.controller = Player_Controller()
        self.map = C_Model.Game_OLD()
        self.view = D_View.View(title="Maze Game", width=35, height=22)

        # build = True
        # self.map.map_initialize()
        # lights = C_self.model.Lights(self.model)
        # self.Controller = B_Controller.Player_Controller()

    # TODO run

    # TODO _run

    def run(self):
        # RUN
        while True:
            # CONTROLLER
            self.controller.playerControllerEvents(self.map)

            # self.model (AKA LEVEL)
            self.map.set_climb_positions_visited(self.map.tuple_current_position, self.map.list_climb_positions, self.map.climb_positions_visited)
            # self.model.set_previous_position()

            self.map.set_lights_debug(lights_state, self.map.brightness_list)
            self.map.set_lights_sun(self.map.tuple_maze_start_position, self.map.paths, self.map.sun_light_positions, self.map.brightness_list, self.map.tuple_maze_finish_position)
            self.map.character_light_positions = self.map.update_character_light_positions(
                self.map.character_light_positions, self.map.tuple_current_position, self.map.paths, self.map.brightness_list)
            self.map.light_positions = self.map.update_light_positions(self.map.paths, self.map.sun_light_positions, self.map.character_light_positions, self.map.light_positions)

            # self.view (AKA DRAW)
            self.view.draw_level(self.map)
            self.view.draw_coordinates(self.controller.mousePos)
            self.view.current_position = self.map.tuple_current_position  # TODO TEMP FIX!!!!!!

            self.view.run(self.map, run_debug_state, self.controller)

            self.clock.tick(60)  # TODO Check what this is doing!!!

    # TODO get state / event

    # TODO update (run objecet's update)

    # TODO paint/draw (clear >  run object's paint)

    # TODO end

    # TODO add object

    # TODO remove object


class Player_Controller():
    def __init__(self):
        self.run = True
        self.select_location = (0, 0)
        self.mousePos = (0, 0)

    def events(self, character):
        x, y = character.tuple_current_position
        res = False
        self.mousePos = pygame.mouse.get_pos()
        self.mousePos = (self.mousePos[0]//GRID_SIZE) * \
            GRID_SIZE, (self.mousePos[1]//GRID_SIZE)*GRID_SIZE
        # print(mousePos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    res = "K_UP"
                elif event.key == pygame.K_DOWN:
                    res = "K_DOWN"
                elif event.key == pygame.K_LEFT:
                    res = "K_LEFT"
                elif event.key == pygame.K_RIGHT:
                    res = "K_RIGHT"
                elif event.key == pygame.K_BACKQUOTE:
                    res = "K_BACKQUOTE"
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x, y = pos
                x_grid = (x // GRID_SIZE) * GRID_SIZE
                y_grid = (y // GRID_SIZE) * GRID_SIZE
                self.select_location = (x_grid, y_grid)
                res = (x_grid, y_grid)

            elif event.type == pygame.QUIT:
                self.run = False
        return res

    def end(self):
        pygame.quit()
        sys.exit()

    def playerControllerEvents(self, level):
        res = self.events(level)
        if not res:
            return

        if res in level.set_position_keys:
            level.set_position(res)
        # elif res == game.game_keys:
        #     game.run_debug_state = not game.run_debug_state
        #     game.lights_state = not game.lights_state ##TODO replace somewhere?
        elif res == level.tuple_current_position:
            print("select")
        elif res not in level.paths or res not in level.camp_positions:
            level.set_route(level.tuple_current_position, res, level)
            # if game.ai_controller_01.route_list[self.route_list_index:] == True:
            index = 1
            for i in level.list_route[level.list_route_index:]:  # TODO need breaking into steps
                index += 1
                level.set_position(i)
                # game.lights.set_lights(game.lights_state)
                self.route_list_index = + 1
                print("wooop", index)
                # break
                # self.run_draw() ##TODO  replace with something else???


def main():
    game_new = Game_NEW()
    game_new.initialize()
    game_new.run()


if __name__ == '__main__':
    main()
