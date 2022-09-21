# from src import event
from src.level.level import Level
from src.view.view import View

from dataclasses import dataclass

# @dataclass
# class View_Data:
#     keyboard_set_position: str
#     mouse_event_run: str






    # Debugs:
run_debug_state = False

# game state controllers:


level = Level()
# model and views:
view = View()

# self.view.setup_view_event_handlers()

# TODO _run/update too?

def update(keyboard_set_position, mouse_event_run) -> None:
    state = "build"

    while True:
        if state == "build":
            level.update_build()
            state = "run"
        if state == "run":
            level.update_run(keyboard_set_position, mouse_event_run)

            keyboard_set_position, mouse_event_run = view.update(
                level,
                run_debug_state,
                level.path_obj.player_path_position,
            )

# TODO get state / event
# TODO update (run object's update)
# TODO end
# TODO add object
# TODO remove object



