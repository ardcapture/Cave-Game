

import Model
import View




DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]


LevelStates = ["01_Title", "02_Settings", "03_Build", "04_Play"]
game_keys = "K_BACKQUOTE"


# build_debug = True


# TODO may not get used!
state = {
    # "title": title,
    # "level_build": build,
    # "level_run": level_run,
    # "level_pause": level_pause
}


class Game:
    def __init__(self):

        # Debugs:
        self.run_debug_state = False

        # game state controllers:

        self.level = Model.Level(self)
        # model and views:
        self.view = View.View(self)


    # TODO _run too?

    def initialize(self):
        pass

    def run(self):
        # RUN
        while True:
            self.level.update()
            self.view.update(self.level, self.run_debug_state)

    # TODO get state / event
    # TODO update (run objecet's update)
    # TODO end
    # TODO add object
    # TODO remove object


def main():
    game_new = Game()
    game_new.run()


if __name__ == '__main__':
    main()
