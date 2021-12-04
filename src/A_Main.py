import pygame

import B_Level
import C_Draw
import D_Controller


class Game():
    def __init__(self):
        self.game_keys = "K_BACKQUOTE"
        self.run_debug_state = True
        self.lights_state = False

    def event_player_controller(self):
        res = self.player_controller.events()
        if res != False:
            if res in self.character.set_position_keys:
                self.character.set_position(res)
            elif res == self.game_keys:
                self.run_debug_state = not self.run_debug_state
                self.lights_state = not self.lights_state
            elif res == self.character.current_poistion:
                print("select")
            elif res in self.level.paths or res in self.level.camp_positions:
                self.ai_controller_01.set_route(self.character.current_poistion, res)
                for i in self.ai_controller_01.route_list:
                    self.character.set_position(i)
                    self.lights.set_lights(self.lights_state)
                    self.run_draw()

    def build(self, build_debug):
        build = True
        while build:
            self.level = B_Level.Level()
            self.MazeBuild(build_debug)
            if self.level.maze_finish_position == (0, 0) or self.level.maze_start_position == (0, 0):
                # self.draw.draw_reset() #TODO MOVE?
                del self.level
            else:
                build = False
        self.character = B_Level.Character(self.level)
        self.lights = B_Level.Lights(self.level, self.character)
        self.draw = C_Draw.Draw(self.level)
        self.player_controller = D_Controller.Player_Controller(self.level, self.character)
        self.ai_controller_01 = D_Controller.AI_Controller(self.level, self.character, self.player_controller)
        self.lights.set_tileImages()
        self.lights.set_route_light_positions(self.level.path_adjacent)
        self.lights.set_route_light_positions_tiles(self.lights.route_light_positions, debug='FALSE')

    def run_set(self):
        self.character.set_climb_positions_visited()
        self.character.set_previous_position
        self.character.set_selected()
        self.lights.set_lights(self.lights_state)
        self.draw.draw_level(self.lights.route_light_positions_tiles)
        self.draw.draw_coordinates(self.player_controller.mousePos)
        self.draw.current_poistion = self.character.current_poistion  # TODO TEMO FIX!!!!!!

    def run_draw(self):
        # DRAW PLAYER
        self.draw.draw_player()

        # DRAW FORGROUND
        self.draw.draw_water()

        self.draw.draw_light_positions(self.lights)
        self.run_debug()

        self.draw.draw_screen()

    def run_debug(self):
        self.draw.draw_debug_start_position(self.run_debug_state)
        self.draw.draw_debug_climb_positions(self.run_debug_state)
        self.draw.draw_debug_ends(self.ai_controller_01, self.run_debug_state)
        self.draw.draw_debug_route(self.ai_controller_01, self.run_debug_state)

    # TODO MAYBE STAY HERE?!

    def MazeBuild(self, build_debug):
        self.level.set_grid()
        mazebuild = True
        while mazebuild == True:
            # self.draw.draw_build_grid(build_debug) #TODO MOVE?
            # self.draw.draw_screen() #TODO MOVE?
            self.level.set_current_position()
            self.level.set_past_positions()
            self.level.set_next_position()
            self.level.set_wall_break_positions()
            # self.draw.draw_build_wall_break_positions(build_debug) #TODO MOVE?
            if len(self.level.past_positions) > 2 and self.level.current_poistion == self.level.past_positions[0]:
                self.level.set_maze_start_position()
                self.level.set_maze_finish_position()
                self.level.set_camp_positions()
                self.level.set_tileLocations()
                self.level.set_paths()
                self.level.set_path_adjacent()
                self.level.set_tiles()
                self.level.setWater()
                self.level.set_climb()
                # self.draw.draw_build_grid_hide(build_debug) #TODO MOVE?
                mazebuild = False


def main():
    clock = pygame.time.Clock()

    game = Game()

    game.build(build_debug=False)

    # def build(self, build_debug):
    
    # build_debug = False
    # build = True
    # while build:
    #     level = B_Level.Level()
    #     game.MazeBuild(build_debug)
    #     if level.maze_finish_position == (0, 0) or level.maze_start_position == (0, 0):
    #         # self.draw.draw_reset() #TODO MOVE?
    #         del level #TODO NOT SURE WILL WORK AS NOW VARIABLE NOT CLASS!!!
    #     else:
    #         build = False
    # character = B_Level.Character(level)
    # lights = B_Level.Lights(level, character)
    # draw = C_Draw.Draw(level)
    # player_controller = D_Controller.Player_Controller(level, character)
    # ai_controller_01 = D_Controller.AI_Controller(level, character, player_controller)
    # lights.set_tileImages()
    # lights.set_route_light_positions(level.path_adjacent)
    # lights.set_route_light_positions_tiles(lights.route_light_positions, debug='FALSE')




    # RUN
    while True:
        game.run_set()
        game.run_draw()
        game.event_player_controller()

        clock.tick(60)


if __name__ == '__main__':
    main()
