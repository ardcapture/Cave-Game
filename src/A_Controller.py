import logging

import C_Model
import D_View

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable()


logging.debug("This is the start of the program!**************************************")


DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]


LevelStates = ["01_Title", "02_Settings", "03_Build", "04_Play"]
game_keys = "K_BACKQUOTE"
run_debug_state = False

build_debug = False


# TODO may not get used!
state = {
    # "title": title,
    # "level_build": build,
    # "level_run": level_run,
    # "level_pause": level_pause
}


class Controller_Game:
    def __init__(self):
        logging.debug('Game_NEW > __init__')

    # TODO Game methods **************************:

    # TODO initalize (instantiate game's class, and there instances)

    def initialize(self):

        self.level = C_Model.Level()
        self.window = D_View.Window(title="Maze Game", width=35, height=22)
        self.view = D_View.View(window=self.window)

        self.controller = D_View.Input_Controller(self.level)

        # build = True
        # self.map.map_initialize()
        # lights = C_self.model.Lights(self.model)
        # self.Controller = B_Controller.Player_Controller()

    # TODO run

    # TODO _run

    def run(self):
        # RUN
        while True:
            # CONTROLLER
            self.controller.events()

            # self.model (AKA LEVEL)
            self.level.set_climb_positions_visited(self.level.tuple_current_position, self.level.list_climb_positions, self.level.climb_positions_visited)
            # self.model.set_previous_position()

            self.level.lights.run()

            # self.view (AKA DRAW)
            self.view.draw_level(self.level)
            self.view.current_position = self.level.tuple_current_position  # TODO TEMP FIX!!!!!!

            self.view.run(self.level, run_debug_state, self.controller)

    # TODO get state / event

    # TODO update (run objecet's update)

    # TODO paint/draw (clear >  run object's paint)

    # TODO end

    # TODO add object

    # TODO remove object


def main():
    logging.debug('def main()')
    game_new = Controller_Game()
    game_new.initialize()
    game_new.run()


if __name__ == '__main__':
    main()
