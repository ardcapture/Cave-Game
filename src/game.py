from src.level import Level
from src.View import View
from src.position import Position
import src.utilities as utilities
import pygame


class Game:
    # Debugs:
    run_debug_state = True

    level = Level()
    view = View(level)

    # TODO _run/update too?

    KEY_DOWN = pygame.K_DOWN
    KEY_LEFT = pygame.K_LEFT
    KEY_UP = pygame.K_UP
    KEY_RIGHT = pygame.K_RIGHT

    def __init__(self) -> None:
        self.state = "build"

        while True:
            if self.state == "build":
                self.state = "run"
            if self.state == "run":
                self.level.set_visited_climb_positions()

                self.level.lights.sun_light_positions = (
                    self.level.get_sunlight_positions()
                )
                self.level.set_character_light_positions()
                self.level.lights.set_light_objs()
                self.set_player_path_position()

                self.view.clear_blit_list()

                self.view.surround.set_path_adjacent(self.level)
                # view.surround.set_poss_surround_positions(self.level)

                self.view.set_route_light_positions_tiles(self.level)
                self.view.update_window_events()

                self.view.set_window_end()

                #! DRAW WINDOW START

                self.view.draw_level(self.level)  # blit (via set_surface_to_surface)
                self.view.draw_coordinates()  # append list_blit
                self.view.draw_water(self.level.water)  # append list_blit
                self.view.set_surface_to_window(
                    self.level
                )  # blit (via set_surface_to_surface)
                self.view.set_blit_objs(self.level)  # append list_blit

                if self.run_debug_state:
                    self.view.in_list_climb_positions(self.level)  # append list_blit
                    self.view.draw_debug_start_position(
                        self.level
                    )  # draw rect (via draw_outline)
                    self.view.draw_debug_ends(self.level)  # blit
                    self.view.draw_debug_route(
                        self.level
                    )  # draw rect (via draw_outline)

                self.view.Blit()  # run list_blit
                self.view.clock.tick(60)  # TODO Check what this is doing!!!
                self.view.update_display()

    def set_player_path_position(self) -> None:
        self.player_path_position = self.mouse_event_run()

        self.level.player_path_position = self.get_player_path_position(Position(0, 0))

    def mouse_event_run(self) -> Position:
        if not self.view.window.mouse_event_run:
            return Position(-1, -1)

        position = self.view.window.mouse_event_run
        position = utilities.position_to_grid_position(position, self.level.GRID_SIZE)

        if (
            position not in self.level.paths.positions
            or position not in self.level.camp_positions
        ):
            current_positions = [self.level.player_path_position]
            updated_positions = self.level.set_route_positions(
                position, self.level.camp_positions
            )
            self.route = self.level.nav.set_route(current_positions, updated_positions)
            route_index = 0
            for i in self.route[route_index:]:  # TODO need breaking into steps
                self.player_path_position = self.get_player_path_position(i)
        return self.level.player_path_position

    def get_player_path_position(self, position: "Position") -> Position:
        x, y = self.level.player_path_position

        if position != Position(0, 0):
            x, y = position

        elif self.view.window.event_keyboard == self.KEY_LEFT:
            x -= self.level.GRID_SIZE
        elif self.view.window.event_keyboard == self.KEY_RIGHT:
            x += self.level.GRID_SIZE
        elif self.view.window.event_keyboard == self.KEY_UP:
            y -= self.level.GRID_SIZE
        elif self.view.window.event_keyboard == self.KEY_DOWN:
            y += self.level.GRID_SIZE

        if (
            Position(x, y) in self.level.paths.positions
            or Position(x, y) in self.level.camp_positions
        ):
            return Position(x, y)

        else:
            return Position(0, 0)


# TODO get state / event
# TODO update (run object's update)
# TODO end
# TODO add object
# TODO remove object
