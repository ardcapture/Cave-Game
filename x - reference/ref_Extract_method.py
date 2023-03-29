class fish:
    def getOutstanding():
        pass

    def name():
        pass

    def printBanner():
        pass

    def printOwing(self):
        self.printBanner()
        self.printDetails(self.getOutstanding())

    def printDetails(self, outstanding):
        print("name:", self.name)
        print("amount:", outstanding)
