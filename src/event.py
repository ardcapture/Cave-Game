class Environment:
    def __init__(self) -> None:
        self.subscribers = dict()

    def connect_objects(self, game, view, level):
        self.game = game
        self.view = view
        self.level = level

    def update(self):
        while True:
            self.game.update_check(self)
            self.view.update_check(self)
