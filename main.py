from games.closest_to_one_hundred import ClosestToOneHundred
import player


class Main:
    def __init__(self):
        print("""
Welcome to the casino!
1. Play game: closest to 100.
2. Display player statistics.
3. Exit the casino.
""")  # fmt: skip

        while True:
            playerSelection = input("Select an available option from the menu: ").strip()  # fmt: skip

            if playerSelection.isdigit():
                playerSelection = int(playerSelection)

                if playerSelection == 1:
                    self.game = ClosestToOneHundred()
                    self.game.gameStart()
                elif playerSelection == 2:
                    self.player = player.Player()
                    print(self.player.getPlayerStatistics())
                    exit()
                elif playerSelection == 3:
                    print("Okay goodbye.")
                    exit()
                else:
                    print("Invalid selection.")
            else:
                print("Invalid selection.")


if __name__ == "__main__":
    Main()
