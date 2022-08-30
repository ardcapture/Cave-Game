import View
import event

from level import Level


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


DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]

GRID_SIZE = View.GRID_SCALE

WIDTH, HEIGHT = (GRID_SIZE * 2) + (GRID_SIZE * 35), (GRID_SIZE * 2) + (GRID_SIZE * 22)
TOP_OFFSET = 5
AROUND = [-1, 0, 1]


COLOURS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "BLACK_VERY_LIGHT": (210, 210, 210),
    "WHITE_4TH_4TH_4TH_4TH": (1, 1, 1),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "BLUE_LIGHT": (125, 125, 255),
    "BLUE_VERY_LIGHT": (210, 210, 255),
}


class Game():
    def __init__(self, env):

        self.updated = False

        self.env = env

        print(f"{self.env=}")

        # Debugs:
        self.run_debug_state = False

        # game state controllers:

        self.keyboard_set_position = None
        self.mouse_event_run = None

        # self.level = level.Level(self)
        # model and views:


    # TODO _run/update too?

    def update_check(self, env):
        if self.env.view.updated:
            self.update(self, env)
            


    def update(self):
        state = "build"

        while True:
            if state == "build":
                self.env.level = self.env.level.update_build()
                state = "run"
            if state == "run":
                self.env.level.update_run(self.keyboard_set_position, self.mouse_event_run)

                # update view
                self.keyboard_set_position, self.mouse_event_run = post_event(
                    "update", self, self.level, self.level.path_obj
                )
            




    # TODO get state / event
    # TODO update (run object's update)
    # TODO end
    # TODO add object
    # TODO remove object


def main():
    mainEnv = event.Environment()


    game_new = Game(mainEnv)
    view = View.View(mainEnv)
    level = Level(mainEnv)

    mainEnv.connect_objects(game_new, view, level)


    # view.setup_view_event_handlers()

    mainEnv.update()


if __name__ == "__main__":
    main()
