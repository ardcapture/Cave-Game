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
    def __init__(self):
        self.run = True
        self.select_location = (0, 0)
        self.mousePos = (0, 0)

    def events(self, character):
        x, y = character.tuple_current_position
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

    def playerControllerEvents(self, level):
        res = self.events(level)
        if res != False:
            if res in level.set_position_keys:
                level.set_position(res)
            # elif res == game.game_keys:
            #     game.run_debug_state = not game.run_debug_state
            #     game.lights_state = not game.lights_state ##TODO replace somewhere?
            elif res == level.tuple_current_position:
                print("select")
            elif res in level.paths or res in level.camp_positions:
                level.set_route(level.tuple_current_position, res, level)
                # if game.ai_controller_01.route_list[self.route_list_index:] == True:
                for i in level.list_route[level.list_route_index:]:  # TODO need breaking into steps
                    level.set_position(i)
                    # game.lights.set_lights(game.lights_state)
                    self.route_list_index = + 1
                    print("wooop")
                    # break
                    # self.run_draw() ##TODO  replace with something else???
