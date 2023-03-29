from typing import TYPE_CHECKING

from src.Level import Level

if TYPE_CHECKING:
    from src.View import View


class Game:
    # Debugs:
    run_debug_state = True

    # game state controllers:

    level = Level()
    # model and views:
    # view = View()

    # self.view.setup_view_event_handlers()

    # TODO _run/update too?

    def __init__(self, view: "View") -> None:
        self.view = view

    def update(self) -> None:

        state = "build"
        self.view.setup(self.level)

        while True:
            if state == "build":
                state = "run"
            if state == "run":
                self.level.set_visited_climb_positions()
                self.level.update(self.view.window)

                # TODO self.level.path should not be here?!
                self.view.update(
                    self,
                    self.level,
                    self.level.nav,
                    self.view.window,
                )


# TODO get state / event
# TODO update (run object's update)
# TODO end
# TODO add object
# TODO remove object
