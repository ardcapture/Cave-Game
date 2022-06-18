import pygame
import random

import B_Controller
import C_Model
import D_View


LevelStates = ["01_Title", "02_Settings", "03_Build", "04_Play"]
game_keys = "K_BACKQUOTE"
run_debug_state = True
lights_state = False
build_debug = True


def build():
    pass


# TODO may not get used!
state = {
    # "title": title,
    "level_build": build,
    # "level_run": level_run,
    # "level_pause": level_pause
}


def main():
    clock = pygame.time.Clock()

    build = True
    while build:
        Controller = B_Controller.Player_Controller()
        level = C_Model.Level()
        draw = D_View.Draw()

        level.set_grid_v01()
        level.set_grid_v02()

        # draw.draw_build_grid(level)  # TODO MOVE?
        draw.draw_v02(level)

        # LOOP
        mazebuild = True
        while mazebuild:
            level.set_current_position()
            level.set_current_position_v02()
            # print("level.current_position_v02: ", level.current_position_v02)
            level.set_past_positions()
            level.set_past_positions_v02()
            level.set_next_position()
            level.set_next_position_v02()
            level.set_wall_break_positions()
            level.set_wall_break_positions_v02()
            if len(level.past_positions) > 2 and level.current_position == level.past_positions[0]:
                mazebuild = False
            # if len(level.past_positions_v02) > 2 and level.current_position_v02 == level.past_positions_v02[0]:
            #     mazebuild_v02 = False

            # draw.draw_build_wall_break_positions(level, build_debug)  # TODO MOVE?

            draw.draw_v02(level)
            # draw.draw_screen()  # TODO MOVE?

        level.set_maze_start_position()
        level.set_maze_start_position_v02()
        level.set_maze_finish_position()
        level.set_maze_finish_position_v02()

        level.set_camp_positions() # not required in v02
        level.set_tileLocations() #used in v02 too
        level.set_paths()
        level.set_paths_v02_obj_navigable()
        level.set_path_adjacent()  # todo may remove
        level.set_tiles()
        level.set_tiles_v02_obj_textures()
        # level.setWater() #todo turn back on in a bit
        # level.set_climb() #todo turn back on in a bit

        draw.draw_build_grid_hide(level, build_debug)  # TODO MOVE?

        if level.maze_finish_position == (0, 0) or level.maze_start_position == (0, 0):
            draw.draw_reset()  # TODO MOVE?
            del level
        else:
            build = False

    level.current_position = random.choice(level.camp_positions)

    lights = C_Model.Lights(level)
    # self.Controller = B_Controller.Player_Controller()

    level.set_navigation(level)

    lights.set_tileImages()
    lights.set_route_light_positions(level.path_adjacent)
    lights.set_route_light_positions_tiles(lights.route_light_positions, debug='FALSE')

    # RUN
    while True:
        # CONTROLLER
        Controller.playerControllerEvents(level)

        # MODEL (AKA LEVEL)
        level.set_climb_positions_visited()
        level.set_previous_position

        lights.set_lights_debug(lights_state)
        lights.set_lights_sun(level)
        lights.set_lights_character(level)
        lights.set_light_positions()

        # VIEW (AKA DRAW)
        draw.draw_level(level, lights)
        draw.draw_coordinates(Controller.mousePos)
        draw.current_position = level.current_position  # TODO TEMP FIX!!!!!!

        draw.draw_player()
        draw.draw_water(level)
        draw.draw_light_positions(lights)
        draw.draw_debug_start_position(level, run_debug_state)
        draw.draw_debug_climb_positions(level, run_debug_state)
        draw.draw_debug_ends(level, run_debug_state)
        draw.draw_debug_route(level, run_debug_state)
        draw.draw_screen()

        clock.tick(60)  # TODO Check what this is doing!!!


if __name__ == '__main__':
    main()
