from src.Game import Game
from src.View import View


def main():
    game = Game(View())
    game.update()


if __name__ == "__main__":
    main()
