from games.game_100 import Game100
from games.game_21 import Game21
from games.game_100_to_0 import Game100To0
from games.game_slots import GameSlots
from utilities.information import printMenu, exitCasino
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
                    self.game = Game100To0(player=self.player, house=self.house)
                    self.game.gameStart()
                elif playerSelection == 4:
                    self.game = GameSlots(player=self.player, house=self.house)
                    self.game.gameStart()
                elif playerSelection == 100:
                    print(self.player.getPlayerStatistics())
                elif playerSelection == 101:
                    self.player.resetPlayerData()
                elif playerSelection == 102:
                    self.house.resetHouseData()
                elif playerSelection == 0:
                    exitCasino(self)
                else:
                    errorHandler()
            else:
                errorHandler()


if __name__ == "__main__":
    Main()
