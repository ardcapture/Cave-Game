import pygame
import random

import B_Controller
import C_Model
import D_View


class Game():
    def __init__(self):
        self.LevelStates = ["01_Title", "02_Settings", "03_Build", "04_Play"]
        self.game_keys = "K_BACKQUOTE"
        self.run_debug_state = True
        self.lights_state = False

    def build(self, build_debug):
        
        build = True
        while build:
            self.Controller = B_Controller.Player_Controller()
            self.level = C_Model.Level()
            self.draw = D_View.Draw()

            self.level.set_grid_set()  #TODO TRYING SOMEHITNG HERE!
            self.level.set_grid_loop() #TODO TRYING SOMEHITNG HERE!

            self.draw.draw_build_grid(self.level)  # TODO MOVE?

            #LOOP
            mazebuild = True
            while mazebuild:
                self.level.set_current_position()
                self.level.set_past_positions()
                self.level.set_next_position()
                self.level.set_wall_break_positions()
                if len(self.level.past_positions) > 2 and self.level.current_poistion == self.level.past_positions[0]:
                    mazebuild = False

                self.draw.draw_build_wall_break_positions(self.level, build_debug)  # TODO MOVE?
                self.draw.draw_screen()  # TODO MOVE?

            self.level.set_maze_start_position()
            self.level.set_maze_finish_position()
            self.level.set_camp_positions()
            self.level.set_tileLocations()
            self.level.set_paths()
            self.level.set_path_adjacent()
            self.level.set_tiles()
            self.level.setWater()
            self.level.set_climb()

            self.draw.draw_build_grid_hide(self.level, build_debug)  # TODO MOVE?

            if self.level.maze_finish_position == (0, 0) or self.level.maze_start_position == (0, 0):
                self.draw.draw_reset()  # TODO MOVE?
                del self.level
            else:
                build = False

        self.level.current_poistion = random.choice(self.level.camp_positions)

        self.lights = C_Model.Lights(self.level)
        # self.Controller = B_Controller.Player_Controller()

        self.level.set_navigation(self.level)

        self.lights.set_tileImages()
        self.lights.set_route_light_positions(self.level.path_adjacent)
        self.lights.set_route_light_positions_tiles(self.lights.route_light_positions, debug='FALSE')


def main():

    clock = pygame.time.Clock()

    game = Game()

    game.build(build_debug=True)


    

    # RUN
    while True:
        # CONTROLLER
        game.Controller.playerControllerEvents(game.level)

        # MODEL (AKA LEVEL)
        game.level.set_climb_positions_visited()
        game.level.set_previous_position

        game.lights.set_lights_debug(game.lights_state)
        game.lights.set_lights_sun(game.level)
        game.lights.set_lights_character(game.level)
        game.lights.set_light_positions()

        # VIEW (AKA DRAW)
        game.draw.draw_level(game.level, game.lights)
        game.draw.draw_coordinates(game.Controller.mousePos)
        game.draw.current_poistion = game.level.current_poistion  # TODO TEMP FIX!!!!!!

        game.draw.draw_player()
        game.draw.draw_water(game.level)
        game.draw.draw_light_positions(game.lights)
        game.draw.draw_debug_start_position(game.level, game.run_debug_state)
        game.draw.draw_debug_climb_positions(game.level, game.run_debug_state)
        game.draw.draw_debug_ends(game.level, game.run_debug_state)
        game.draw.draw_debug_route(game.level, game.run_debug_state)
        game.draw.draw_screen()

        clock.tick(60)  # TODO Check what this is doing!!!


if __name__ == '__main__':
    main()
