from games.game100 import Game100
from games.game21 import Game21
from utilities.information import printMenu
from utilities.errors import errorHandler
import player
import house


class Main:
    def __init__(self):
        self.player = player.Player()
        self.house = house.House()

        while True:
            printMenu(self)
            playerSelection = input("Select an available option from the menu: ").strip()  # fmt: skip

            if playerSelection.isdigit():
                playerSelection = int(playerSelection)

                if playerSelection == 1:
                    self.game = Game100(player=self.player, house=self.house)
                    self.game.gameStart()
                elif playerSelection == 2:
                    self.game = Game21(player=self.player, house=self.house)
                    self.game.gameStart()
                elif playerSelection == 3:
                    print(self.player.getPlayerStatistics())
                elif playerSelection == 4:
                    self.player.resetPlayerData()
                elif playerSelection == 5:
                    self.house.resetHouseData()
                elif playerSelection == 6:
                    print("Okay goodbye.")
                    exit()
                else:
                    errorHandler()
            else:
                errorHandler()


if __name__ == "__main__":
    Main()
