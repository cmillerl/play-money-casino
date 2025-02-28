from utilities import errors


def displayGameInformation(self):
    """
    Display the game information for the current game the player is playing.
    """
    while self.count < 1:
        userSelection = (input("Do you want to read the games description?\n")).lower().strip()  # fmt: skip
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
            userSelection = input("Do you want to start the game?\n").lower().strip()  # fmt: skip
            if userSelection in ["yes", "y"]:
                break
            elif userSelection in ["no", "n"]:
                print("Okay, goodbye!")
                exit()
            else:
                errors.errorHandler()
