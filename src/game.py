from typing import TYPE_CHECKING

from src.level import Level

if TYPE_CHECKING:
    from src.view import View


class Game:
    # Debugs:
    run_debug_state = True

    # game state controllers:

    level = Level()
    # model and views:
    # view = View()

    # self.view.setup_view_event_handlers()

    # TODO _run/update too?

    def __init__(self) -> None:
        pass

    def update(self, view: "View") -> None:
        state = "build"
        view.setup(self.level)

        while True:
            if state == "build":
                state = "run"
            if state == "run":
                self.level.set_visited_climb_positions()

                self.level.set_light_positions()
                self.level.set_characterLightPositions()
                self.level.set_sun_light_positions()

                self.level.update(view.window)

                # TODO self.level.path should not be here?!
                view.clear_blit_list()
                view.surround.update(self.level)
                view.set_route_light_positions_tiles()
                view.set_pygame_events()
                view.window.set_m_event()
                view.set_window_end()

                #! DRAW WINDOW START

                view.draw_level(self.level)  # blit (via set_surface_to_surface)
                view.draw_coordinates()  # append list_blit
                view.draw_water(self.level.water)  # append list_blit
                view.set_surface_to_window(
                    self.level
                )  # blit (via set_surface_to_surface)
                view.set_blit_objs(self.level)  # append list_blit

                if self.run_debug_state:
                    view.in_list_climb_positions(self.level)  # append list_blit
                    view.draw_debug_start_position(
                        self.level
                    )  # draw rect (via draw_outline)
                    view.draw_debug_ends(self.level)  # blit
                    view.draw_debug_route(self.level)  # draw rect (via draw_outline)

                view.Blit()  # run list_blit
                view.clock.tick(60)  # TODO Check what this is doing!!!
                view.update_display()


# TODO get state / event
# TODO update (run object's update)
# TODO end
# TODO add object
# TODO remove object
