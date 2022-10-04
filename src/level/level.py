from src.water import Water
from src import utilities
from typing import TYPE_CHECKING


from src.level.build import Paths_Build
from src.level.lights import Lights
from src.level.path import Path


if TYPE_CHECKING:
    from src.view import Keyboard, Mouse
    from src.utilities import Position


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


KEY_LEFT = "K_LEFT"
KEY_RIGHT = "K_RIGHT"
KEY_UP = "K_UP"
KEY_DOWN = "K_DOWN"


class Level:

    GRID_SIZE = 32
    GRID_SIZE_2D = (GRID_SIZE, GRID_SIZE)
    WIDTH_GS = (GRID_SIZE * 2) + (GRID_SIZE * 35)
    HEIGHT_GS = (GRID_SIZE * 2) + (GRID_SIZE * 22)
    # TOP_OFFSET = 5

    def __init__(self):

        self.objs = []
        self.top_offset = 5

        self.path_climb_positions_visited = []
        self.lights_state = False

        self.previous_position = ()
        self.selected = False
        self.velocity = self.GRID_SIZE

        self.build = Paths_Build(
            self.GRID_SIZE, self.WIDTH_GS, self.top_offset, self.HEIGHT_GS
        )

        self.build_path_positions = self.build.update()

        self.path = Path()

        self.path.update_build(self)

        if self.path.reset:
            self.reset()
            pass

        self.lights = Lights(self)
        self.water = Water()

        self.route = []

    def update_build(self):

        self.water.update(self, path=self.path)

    def update_run(self, keyboard: "Keyboard", mouse: "Mouse"):

        self.path_climb_positions_visited = self.path.update_run(
            climb_positions=self.path.list_climb_positions,
            player_path_position=self.path.player_path_position,
            path_climb_positions_visited=self.path_climb_positions_visited,
        )

        self.light_objs = self.lights.update(self, self.path)

        if mouse.mouse_event_run:
            player_path_position = self.mouse_event_run(
                mouse,
                self.path,
                self.path.camp_positions,
                self.path.player_path_position,
                self.path.paths,
                self.path.dict_position_str,
                self.path.dict_position_list_position,
            )

        player_path_position = self.get_player_path_position(
            keyboard,
            self.path.paths,
            self.path.camp_positions,
            self.path.player_path_position,
        )

        self.path.player_path_position = player_path_position

    def reset(
        self,
    ):
        self.__init__()

    #!!!! Class navigation?

    @property
    def water_line(self) -> float:
        return (self.HEIGHT_GS - self.GRID_SIZE * 2) * (2 / 3)

    def mouse_event_run(
        self,
        mouse: "Mouse",
        path,
        camp_positions,
        player_path_position,
        paths,
        path_type,
        path_directions,
    ):

        print(f"mouse event run!!!!")

        position = mouse.mouse_event_run
        grid_size = self.GRID_SIZE
        res = utilities.position_to_grid_position(position, grid_size)

        if res not in paths or res not in camp_positions:

            self.route = self.set_route(
                player_path_position,
                res,
                paths,
                camp_positions,
                path_type,
                path_directions,
            )
            route_index = 0
            index = 1
            for i in self.route[route_index:]:  # TODO need breaking into steps
                index += 1
                player_path_position = self.get_player_path_position(
                    i, paths, camp_positions, player_path_position
                )
        return player_path_position

    def set_route(
        self,
        start: "Position",
        end: "Position",
        paths: list["Position"],
        camp_positions: list["Position"],
        path_type: dict["Position", str],
        path_directions: dict["Position", list["Position"]],
    ):
        """For Nav - currently used in controller."""

        route_list_A = [start]
        if end in paths or end in camp_positions:
            route_list_B = [end]
        else:
            route_list_B = [start]
        run = True
        while run:
            if (
                path_type[route_list_A[-1]] <= path_type[route_list_B[-1]]
                or len(route_list_A) == 0
            ):
                result = max(path_directions[route_list_A[-1]], key=path_type.get)
                route_list_A.append(result)
            if (
                path_type[route_list_B[-1]] <= path_type[route_list_A[-1]]
                or len(route_list_B) == 0
            ):
                result = max(path_directions[route_list_B[-1]], key=path_type.get)
                route_list_B.append(result)
            duplicate = [i for i in route_list_A if i in route_list_B]
            if duplicate:
                route_list_A.pop(-1)
                run = False
        route_list_B.reverse()
        route_list_A.extend(route_list_B)
        return route_list_A

    def get_player_path_position(
        self, keyboard: "Keyboard", paths, camp_positions, player_path_position
    ):

        x, y = player_path_position

        if isinstance(keyboard, tuple):
            x, y = keyboard

        elif keyboard.event_keyboard == KEY_LEFT:
            x -= self.velocity
        elif keyboard.event_keyboard == KEY_RIGHT:
            x += self.velocity
        elif keyboard.event_keyboard == KEY_UP:
            y -= self.velocity
        elif keyboard.event_keyboard == KEY_DOWN:
            y += self.velocity

        if (x, y) in paths or (x, y) in camp_positions:
            return (x, y)

    #!!!! *******************************************
