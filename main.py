from games.game100 import Game100
from games.game21 import Game21
import player


class Main:
    def __init__(self):
        print("""
Welcome to the casino!
1. Play game: 100.
2. Play game: Blackjack.
3. Display player statistics.
4. Exit the casino.
""")  # fmt: skip

        while True:
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
                    self.player = player.Player()
                    print(self.player.getPlayerStatistics())
                    exit()
                elif playerSelection == 4:
                    print("Okay goodbye.")
                    exit()
                else:
                    print("Invalid selection.")
            else:
                print("Invalid selection.")


if __name__ == "__main__":
    Main()
