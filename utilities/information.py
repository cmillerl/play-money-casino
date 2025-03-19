from utilities import errors


def displayGameInformation(self):
    """
    Display the game information for the current game the player is playing.
    """
    while self.count < 1:
        userSelection = (input("Do you want to read the games description? (y/n)\n")).lower().strip()  # fmt: skip
        self.count += 1
        if userSelection in ["yes", "y"]:
            print(self.gameDescription)
        elif userSelection in ["no", "n"]:
            print("Okay, let's start the game.")
            break
        else:
            errors.errorHandler()
            self.count = 0
            self.displayGameInformation()

        while True:
            userSelection = input("Do you want to start the game? (y/n)\n").lower().strip()  # fmt: skip
            if userSelection in ["yes", "y"]:
                break
            elif userSelection in ["no", "n"]:
                exitCasino(self)
            else:
                errors.errorHandler()


def printMenu(self):
    """
    Print the menu for the game.
    """
    print("""
Welcome to the casino!
1. Play game: 100.
2. Play game: Blackjack.
3. Play game: 100 to 0.
4. Play game: Slots.
100. Display player statistics.
101. Reset player data.
102. Reset house data.
0. Exit the casino.
""")  # fmt: skip
    
def exitCasino(self):
    """
    Exit the casino.
    """
    print("Thank you for playing at the casino. Goodbye!")
    exit()
