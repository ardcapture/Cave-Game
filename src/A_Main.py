import pygame

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
            self.level = C_Model.Level()
            self.draw = D_View.Draw(self.level)

            self.level.set_grid()

            self.draw.draw_build_grid()  # TODO MOVE?

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

            self.draw.draw_build_grid_hide(build_debug)  # TODO MOVE?

            if self.level.maze_finish_position == (0, 0) or self.level.maze_start_position == (0, 0):
                self.draw.draw_reset()  # TODO MOVE?
                del self.level
            else:
                build = False

        self.character = C_Model.Character(self.level)
        self.lights = C_Model.Lights(self.level, self.character)

        self.player_controller = B_Controller.Player_Controller(self.level, self.character)
        self.ai_controller_01 = B_Controller.AI_Controller(self.character, self.player_controller)

        self.ai_controller_01.set_navigation(self.level)
        
        self.lights.set_tileImages()
        self.lights.set_route_light_positions(self.level.path_adjacent)
        self.lights.set_route_light_positions_tiles(self.lights.route_light_positions, debug='FALSE')


def main():
    route_list_index = 0

    clock = pygame.time.Clock()

    game = Game()

    game.build(build_debug=True)

    # RUN
    while True:
        # CONTROLLER
        game.player_controller.playerControllerEvents(game.level, game.character, game.ai_controller_01)

        # MODEL (AKA LEVEL)
        game.character.set_climb_positions_visited()
        game.character.set_previous_position
        game.character.set_selected()
        game.lights.set_lights(game.lights_state)

        # VIEW (AKA DRAW)
        game.draw.draw_level(game.lights.route_light_positions_tiles)
        game.draw.draw_coordinates(game.player_controller.mousePos)
        game.draw.current_poistion = game.character.current_poistion  # TODO TEMP FIX!!!!!!

        game.draw.draw_player()
        game.draw.draw_water()
        game.draw.draw_light_positions(game.lights)
        game.draw.draw_debug_start_position(game.run_debug_state)
        game.draw.draw_debug_climb_positions(game.run_debug_state)
        game.draw.draw_debug_ends(game.ai_controller_01, game.run_debug_state)
        game.draw.draw_debug_route(game.ai_controller_01, game.run_debug_state)
        game.draw.draw_screen()

        clock.tick(60)  # TODO Check what this is doing!!!


if __name__ == '__main__':
    main()
