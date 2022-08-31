import View
import level


from event import post_event

# trying more git stuff
# is this git branch working test!


class Game:
    def __init__(self):

        # Debugs:
        self.run_debug_state = False

        # game state controllers:

        self.keyboard_set_position = None
        self.mouse_event_run = None
        self.level = level.Level(self)
        # model and views:
        self.view = View.View(self)

        self.view.setup_view_event_handlers()

    # TODO _run/update too?

    def update(self):
        state = "build"

        while True:
            if state == "build":
                self.level.update_build()
                state = "run"
            if state == "run":
                self.level.update_run(self.keyboard_set_position, self.mouse_event_run)

                self.keyboard_set_position, self.mouse_event_run = post_event(
                    "update",
                    self.level,
                    self.run_debug_state,
                    self.level.path_obj.player_path_position,
                )

    # TODO get state / event
    # TODO update (run object's update)
    # TODO end
    # TODO add object
    # TODO remove object


def main():
    game_new = Game()
    game_new.update()


if __name__ == "__main__":
    main()
