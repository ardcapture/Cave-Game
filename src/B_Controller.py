import pygame
import sys
import keyboard
import mouse

GRID_SIZE = 32

GRID_SIZE = 32

WIDTH, HEIGHT = (GRID_SIZE*2) + (GRID_SIZE *
                                 35), (GRID_SIZE*2) + (GRID_SIZE * 22)


DIRECTIONS = [(0, 1), (-1, 0), (1, 0), (0, -1)]


class Player_Controller():
    def __init__(self, level, character):
        self.character = character
        self.run = True
        self.select_location = (0, 0)
        self.mousePos = (0, 0)

    def events(self):
        x, y = self.character.current_poistion
        res = False
        self.mousePos = pygame.mouse.get_pos()
        self.mousePos = (self.mousePos[0]//GRID_SIZE) * \
            GRID_SIZE, (self.mousePos[1]//GRID_SIZE)*GRID_SIZE
        # print(mousePos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    res = "K_UP"
                elif event.key == pygame.K_DOWN:
                    res = "K_DOWN"
                elif event.key == pygame.K_LEFT:
                    res = "K_LEFT"
                elif event.key == pygame.K_RIGHT:
                    res = "K_RIGHT"
                elif event.key == pygame.K_BACKQUOTE:
                    res = "K_BACKQUOTE"
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x, y = pos
                x_grid = (x // GRID_SIZE) * GRID_SIZE
                y_grid = (y // GRID_SIZE) * GRID_SIZE
                self.select_location = (x_grid, y_grid)
                res = (x_grid, y_grid)

            elif event.type == pygame.QUIT:
                self.run = False
        return res

    def playerControllerEvents(self, level, character, ai_controller):
        res = self.events()
        if res != False:
            if res in character.set_position_keys:
                character.set_position(res)
            # elif res == game.game_keys:
            #     game.run_debug_state = not game.run_debug_state
            #     game.lights_state = not game.lights_state ##TODO replace somewhere?
            elif res == character.current_poistion:
                print("select")
            elif res in level.paths or res in level.camp_positions:
                ai_controller.set_route(character.current_poistion, res, level)
                # if game.ai_controller_01.route_list[self.route_list_index:] == True:
                for i in ai_controller.route_list[ai_controller.route_list_index:]:  # TODO need breaking into steps
                    character.set_position(i)
                    # game.lights.set_lights(game.lights_state)
                    self.route_list_index = + 1
                    print("wooop")
                    # break
                    # self.run_draw() ##TODO  replace with something else???


class AI_Controller():
    def __init__(self, character, player_controller):
        self.character = character
        self.player_controller = player_controller
        self.ends_list = []
        self.path_type = {}
        self.path_directions = {}
        self.route_list = []
        self.route_list_index = 0

    def set_navigation(self, level):
        self.path_type = dict.fromkeys(level.paths, "X")
        self.path_type.update(dict.fromkeys(level.camp_positions, "X"))
        self.path_directions = dict.fromkeys(level.paths, [])
        for p in self.path_type.keys():
            path_directions = []
            for d in DIRECTIONS:
                direction = (p[0] + (d[0] * GRID_SIZE),
                             p[1] + (d[1] * GRID_SIZE))
                if direction in self.path_type:
                    path_directions.append(direction)
            if len(path_directions) == 1:
                self.path_type[p] = 1
                self.path_directions[p] = path_directions
            if len(path_directions) == 2:
                self.path_type[p] = "P"
                self.path_directions[p] = path_directions
            if len(path_directions) > 2:
                self.path_type[p] = "J"
                self.path_directions[p] = path_directions
        for p in [k for k, v in self.path_type.items() if v == 1]:
            if self.path_type[self.path_directions[p][0]] == "P":
                self.path_type[self.path_directions[p][0]] = "N"

        run = True
        while run:
            if any([k for k, v in self.path_type.items() if v == "N"]):
                for k in [k for k, v in self.path_type.items() if v == "N"]:
                    for i in self.path_directions[k]:
                        if isinstance(self.path_type[i], int):
                            result = self.path_type[i]
                        if self.path_type[i] == "P":
                            self.path_type[i] = "N"
                    self.path_type[k] = result + 1
            elif any([k for k, v in self.path_type.items() if v == "G"]):
                for k in [k for k, v in self.path_type.items() if v == "G"]:
                    result = 0
                    result_list02 = []
                    for i in self.path_directions[k]:
                        if isinstance(self.path_type[i], int):
                            result_list02.append(self.path_type[i])
                        if isinstance(self.path_type[i], str):
                            self.path_type[i] = "N"
                    self.path_type[k] = sorted(result_list02)[-1] + 1
            elif any([k for k, v in self.path_type.items() if v == "J"]):
                for k, v in self.path_type.items():
                    if v == "J":
                        result_list = []
                        for i in self.path_directions[k]:
                            if isinstance(self.path_type[i], int):
                                result_list.append(i)
                                if len(result_list) == (len(self.path_directions[k]) - 1):
                                    if self.path_type[k] == "J":
                                        self.path_type[k] = "G"
            else:
                run = False

    def set_route(self, start, end, level):
        route_list_A = []
        route_list_B = []
        route_list_A.append(start)
        if end in level.paths or end in level.camp_positions:
            route_list_B.append(end)
        else:
            route_list_B.append(start)
        run = True
        while run:
            if self.path_type[route_list_A[-1]] <= self.path_type[route_list_B[-1]] or len(route_list_A) == 0:
                result = max(self.path_directions[route_list_A[-1]], key=self.path_type.get)
                route_list_A.append(result)
            if self.path_type[route_list_B[-1]] <= self.path_type[route_list_A[-1]] or len(route_list_B) == 0:
                result = max(self.path_directions[route_list_B[-1]], key=self.path_type.get)
                route_list_B.append(result)
            duplicte = [i for i in route_list_A if i in route_list_B]
            if duplicte:
                route_list_A.pop(-1)
                run = False
        route_list_B.reverse()
        route_list_A.extend(route_list_B)
        self.route_list = route_list_A
