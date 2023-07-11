from src.game import Game
from src.view import View


def main():
    game = Game(View())
    game.update()


if __name__ == "__main__":
    main()
