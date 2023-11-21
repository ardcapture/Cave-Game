from src.game import Game
from src.view import View


def main():
    game = Game()
    view = View()
    game.update(view)


if __name__ == "__main__":
    main()
