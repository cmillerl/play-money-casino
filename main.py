from games.game100 import Game100
from games.game21 import Game21
from utilities.information import printMenu
import player


class Main:
    def __init__(self):
        self.player = player.Player()

        while True:
            printMenu(self)
            playerSelection = input("Select an available option from the menu: ").strip()  # fmt: skip

            if playerSelection.isdigit():
                playerSelection = int(playerSelection)

                if playerSelection == 1:
                    self.game = Game100()
                    self.game.gameStart()
                elif playerSelection == 2:
                    self.game = Game21()
                    self.game.gameStart()
                elif playerSelection == 3:
                    print(self.player.getPlayerStatistics())
                elif playerSelection == 4:
                    self.player.resetPlayerData()
                elif playerSelection == 5:
                    print("Okay goodbye.")
                    exit()
                else:
                    print("Invalid selection.")
            else:
                print("Invalid selection.")


if __name__ == "__main__":
    Main()
