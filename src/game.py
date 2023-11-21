from src.level import Level
from src.view import View

# if TYPE_CHECKING:
#     from src.view import View


class Game:
    # Debugs:
    run_debug_state = True

    # game state controllers:

    level = Level()
    view = View(level)
    # model and views:
    # view = View()

    # self.view.setup_view_event_handlers()

    # TODO _run/update too?

    def __init__(self) -> None:
        self.state = "build"
        # self.view.set_window(self.level)
        # self.view.set_tile(self.level)
        # self.view.set_sky_V02(self.level)
        # self.view.set_rock_V02(self.level)
        # self.view.set_grass_V02(self.level)
        # self.view.set_surround()

        while True:
            if self.state == "build":
                self.state = "run"
            if self.state == "run":
                self.level.set_visited_climb_positions()
                self.level.set_light_positions()
                self.level.set_sun_light_positions()
                self.level.set_character_light_positions()
                self.level.lights.set_light_objs()
                self.level.set_player_path_position(self.view.window)

                self.view.clear_blit_list()

                self.view.surround.set_path_adjacent(self.level)
                # view.surround.set_poss_surround_positions(self.level)

                self.view.set_route_light_positions_tiles(self.level)
                self.view.set_pygame_events()
                self.view.window.set_m_event()
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


# TODO get state / event
# TODO update (run object's update)
# TODO end
# TODO add object
# TODO remove object
