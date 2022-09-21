from src import game

keyboard_set_position = None
mouse_event_run = None


def main():
    game.update(keyboard_set_position, mouse_event_run)
    # game_new = Game()
    # game_new.update()


if __name__ == "__main__":
    main()
