# NOTE trying to convert functions to returning item all variables are arguments
# working through MAIN
# 27 JUN 2022


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
        model = C_Model.Model()
        view = D_View.View()

        # level.grid = level.set_grid_v01(level.top_offset)
        # level.objs = level.set_grid_v02(level.top_offset)

        # draw.draw_build_grid(level)  # TODO MOVE?

        model.list_grid = model.set_grid_v01()
        model.tuple_current_position = random.choice(model.list_grid)

        view.draw_v02(model)

        # LOOP
        mazebuild = True
        while mazebuild:

            # ! V01

            model.set_maze(model.list_past_positions, model.tuple_current_position, model.list_grid, model.list_path_return, model.list_wall_break_positions, model.list_next_position)

            mazebuild = model.check_maze_finish(model.list_past_positions, model.tuple_current_position)

            # view.draw_build_wall_break_positions(model, build_debug)  # TODO MOVE?

            # view.draw_screen()  # TODO MOVE?

            # ! V02
            #! level.past_positions_v02.append(level.current_position_v02)
            #! level.next_position_v02 = level.set_next_position_v02(level.current_position_v02, level.past_positions_v02, level.path_return_v02)
            #! level.update_wall_break_positions_v02_obj(level.next_position_v02, level.current_position_v02)
            #! level.current_position_v02 = level.set_current_position_v02(level.current_position_v02, level.next_position_v02)
            #! view.draw_v02(model)

            # if len(model.past_positions) > 2 and model.current_position == model.past_positions[0]:
            #     mazebuild = False
            # if len(level.past_positions_v02) > 2 and level.current_position_v02 == level.past_positions_v02[0]:
            #     mazebuild_v02 = False

        #! v01
        model.poss_maze_start = model.set_poss_maze_start(model.list_past_positions)
        model.tuple_maze_start_position = model.set_maze_start_position(model.poss_maze_start)
        model.poss_maze_finish = model.set_poss_maze_finish(model.list_past_positions)
        model.tuple_maze_finish_position = model.set_maze_finish_position(model.poss_maze_finish)

        #! v02
        #! model.update_maze_start_position_v02_obj(model.past_positions_v02, model.top_offset)
        #! model.set_maze_finish_position_v02()

        #! V01
        model.camp_positions = model.set_camp_positions_list(model.tuple_maze_start_position)  # not required in v02
        model.sky = model.set_tileLocations_sky()
        model.rock = model.set_tileLocations_rock()
        model.grass = model.set_tileLocations_grass()
        # level.earth = level.set_tileLocations_earth(level.top_offset) #used in v02 too
        model.paths = model.set_paths(model.list_past_positions, model.list_wall_break_positions, model.tuple_maze_start_position, model.tuple_maze_finish_position)

        model.light_positions = dict.fromkeys(model.paths, (0, 0, 0))
        model.character_light_positions = dict.fromkeys(model.paths, (0, 0, 0))
        # print( 'model.character_light_positions',  model.character_light_positions)
        model.sun_light_positions = dict.fromkeys(model.paths, (0, 0, 0))

        model.path_adjacent = model.set_dict_path_adjacent()  # todo may remove
        model.tiles = model.set_dict_tiles()
        # level.setWater() #todo turn back on in a bit
        # level.set_climb() #todo turn back on in a bit

        #! V02
        #! model.camp_positions_v02 = model.set_tileLocations_camp_positions_v02(model.maze_start_position_v02)
        #! model.paths_v02 = model.set_paths_v02_obj_navigable()
        #! model.set_tiles_v02_obj_textures()

        view.draw_build_grid_hide(model, build_debug)  # TODO MOVE?

        if model.tuple_maze_finish_position == (0, 0) or model.tuple_maze_start_position == (0, 0):
            view.draw_reset()  # TODO MOVE?
            del model
        else:
            build = False

    model.tuple_current_position = random.choice(model.camp_positions)

    # lights = C_Model.Lights(model)
    # self.Controller = B_Controller.Player_Controller()

    model.set_navigation()

    model.set_tileImages()

    model.route_light_positions = model.set_route_light_positions(model.path_adjacent, model.light_positions)
    model.set_route_light_positions_tiles(debug='FALSE')

    # RUN
    while True:
        # CONTROLLER
        Controller.playerControllerEvents(model)

        # MODEL (AKA LEVEL)
        model.set_climb_positions_visited(model.tuple_current_position, model.list_climb_positions, model.climb_positions_visited)
        # model.set_previous_position()

        model.set_lights_debug(lights_state, model.brightness_list)
        model.set_lights_sun(model.tuple_maze_start_position, model.paths, model.sun_light_positions, model.brightness_list, model.tuple_maze_finish_position)
        model.character_light_positions = model.update_character_light_positions(model.character_light_positions, model.tuple_current_position, model.paths, model.brightness_list)
        model.light_positions = model.update_light_positions(model.paths, model.sun_light_positions, model.character_light_positions, model.light_positions)

        # VIEW (AKA DRAW)
        view.draw_level(model)
        view.draw_coordinates(Controller.mousePos)
        view.current_position = model.tuple_current_position  # TODO TEMP FIX!!!!!!

        view.draw_player()
        # view.draw_water(model)
        view.draw_light_positions(model)
        view.draw_debug_start_position(model, run_debug_state)
        view.draw_debug_climb_positions(model, run_debug_state)
        view.draw_debug_ends(model, run_debug_state)
        view.draw_debug_route(model, run_debug_state)
        view.draw_screen()

        clock.tick(60)  # TODO Check what this is doing!!!


if __name__ == '__main__':
    main()
