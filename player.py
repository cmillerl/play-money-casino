import json
import os


class Player:
    def __init__(self, firstName="Player_One"):

        # Player name.
        self.firstName = firstName

        # Initial player bet set to 0.
        self.bet = 0

        self.folderPath = "json_data"
        self.filePath = os.path.join(self.folderPath, "player_data.json")

        # Default player data.
        self.data = {
            "firstName": self.firstName,
            "bankroll": 100000000,
            "gamesWon": 0,
            "gamesLost": 0,
        }

        os.makedirs(self.folderPath, exist_ok=True)

        self.loadPlayerData()

    def loadPlayerData(self):
        """
        Load player data from a JSON file, if not found create a new one.
        """
        if os.path.exists(self.filePath):
            if os.path.getsize(self.filePath) == 0:
                self.savePlayerData()
            else:
                try:
                    with open(self.filePath, "r") as file:
                        self.data = json.load(file)
                except json.JSONDecodeError:
                    self.savePlayerData()
        else:
            self.savePlayerData()

    def savePlayerData(self):
        """
        Save player data to a JSON file.
        """

        with open(self.filePath, "w") as file:
            json.dump(self.data, file, indent=4)

    def getPlayerBet(self):
        """Prompt the player to enter a bet and validate it."""
        while True:
            try:
                bet = input("How much would you like to bet? ").replace(",", "").strip()
                if bet in ["max"]:
                    self.bet = self.data["bankroll"]
                    print(f"You bet: {self.bet:,}")
                    break

                bet = int(bet)
                if bet <= 0:
                    print("Bet must be greater than 0. Try again.")
                elif bet > self.data["bankroll"]:
                    print("You don't have enough funds. Try again.")
                else:
                    self.bet = bet
                    print(f"You bet: {self.bet:,}")
                    break
            except ValueError:
                print("Invalid input! Please enter a number.")

    def updatePlayerBankroll(self, won: bool):
        """Update the players bankroll based on a win or loss."""
        if won:
            self.data["bankroll"] += self.bet
        else:
            self.data["bankroll"] -= self.bet

        self.savePlayerData()

    def displayPlayerBankroll(self):
        """Print the players current bankroll."""
        print(f"Your bankroll: {self.data['bankroll']:,}")

    def winLossRatio(self):
        """Calculate and return the win/loss ratio."""
        if self.data["gamesLost"] == 0:
            return self.data["gamesWon"]
        else:
            return self.data["gamesWon"] / self.data["gamesLost"]

    def continuePlay(self):
        try:
            userSelection = input("Do you want to play again?\n").lower().strip()
            if userSelection in ["yes", "y"]:
                return True
            else:
                print("Okay, goodbye!")
                exit()
        except ValueError:
            print("Invalid input. Please enter yes or no.")
