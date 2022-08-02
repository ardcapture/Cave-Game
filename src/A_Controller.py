import logging

import Model
import View

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable()


logging.debug("This is the start of the program!**************************************")


DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]


LevelStates = ["01_Title", "02_Settings", "03_Build", "04_Play"]
game_keys = "K_BACKQUOTE"


build_debug = False


# TODO may not get used!
state = {
    # "title": title,
    # "level_build": build,
    # "level_run": level_run,
    # "level_pause": level_pause
}


class Controller:
    def __init__(self):

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
            self.level.run()
            self.view.update(self.level, self.run_debug_state)

    # TODO get state / event
    # TODO update (run objecet's update)
    # TODO end
    # TODO add object
    # TODO remove object


def main():
    game_new = Controller()
    game_new.run()


if __name__ == '__main__':
    main()
