# from src import event
from src.level.level import Level
from src.view.view import View


class Game:
    # Debugs:
    run_debug_state = True

    # game state controllers:

    level = Level()
    # model and views:
    view = View(level)

    # self.view.setup_view_event_handlers()

    # TODO _run/update too?

    def update(self) -> None:

        state = "build"

        while True:
            if state == "build":
                self.level.update_build()
                state = "run"
            if state == "run":
                self.level.update_run(self.view.keyboard, self.view.mouse)

                # TODO self.level.path should not be here?!
                self.view.update(
                    self,
                    self.level,
                    self.level.path,
                )


# TODO get state / event
# TODO update (run object's update)
# TODO end
# TODO add object
# TODO remove object
