import json
import os
from utilities.errors import errorHandler
from utilities.information import exitCasino
import house
from time import sleep


class Player:
    def __init__(self, PlayerID=None):

        # Player name.
        if PlayerID is None:
            self.PlayerID = self.getPlayerName()
        else:
            self.PlayerID = PlayerID

        # Initial player bet set to 0.
        self.bet = 0

        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.folderPath = os.path.join(self.directory, "json_data")
        self.filePath = os.path.join(self.folderPath, "player_data.json")

        # Default player data.
        self.data = {
            "playerName": self.PlayerID,
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
            try:
                with open(self.filePath, "r") as file:
                    allData = json.load(file)
                if self.PlayerID in allData:
                    self.data = allData[self.PlayerID]
                else:
                    allData[self.PlayerID] = self.data
                    self.savePlayerData(allData)
            except json.JSONDecodeError:
                print("Error reading JSON File.")
                self.savePlayerData({self.PlayerID: self.data})
        else:
            self.savePlayerData({self.PlayerID: self.data})

    def savePlayerData(self, allData):
        """
        Save player data to a JSON file.
        """

        with open(self.filePath, "w") as file:
            json.dump(allData, file, indent=4)

    def getPlayerBet(self):
        """
        Prompt the player to enter a bet and validate it.
        """
        while True:
            try:
                bet = (
                    input("How much would you like to bet?:\n")
                    .replace(",", "")
                    .replace("$", "")
                    .replace(".", "")
                    .strip()
                )
                if bet in ["max", "all", "maximum"]:
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
                errorHandler(self)

    def updatePlayerBankroll(self, won: bool):
        """
        Update the players bankroll based on a win or loss.
        """
        if won:
            print("Congratulations, you win this round!")
            self.data["bankroll"] += self.bet
            self.data["gamesWon"] += 1
            house.House().data["bankroll"] -= self.bet
            sleep(1)
            self.displayPlayerBankroll()
        else:
            print("Sorry, you lose this round.")
            self.data["bankroll"] -= self.bet
            self.data["gamesLost"] += 1
            house.House().data["bankroll"] += self.bet
            sleep(1)
            self.displayPlayerBankroll()

        with open(self.filePath, "r") as file:
            allData = json.load(file)

        allData[self.PlayerID] = self.data
        self.savePlayerData(allData)

    def displayPlayerBankroll(self):
        """
        Print the players current bankroll.
        """
        print(f"Your bankroll: {self.data['bankroll']:,}")

    def winLossRatio(self, playerData):
        """
        Calculate and return the win/loss ratio.
        """

        wins = playerData.get("gamesWon")
        losses = playerData.get("gamesLost")
        ratio = wins / losses if losses != 0 else wins
        return f"{ratio:.2f}"

    def continuePlay(self):
        """
        Prompt the user to play again or exit.
        """
        if self.data["bankroll"] <= 0:
            print("You are out of funds.")
            exit()
        while True:
            userSelection = input("Do you want to play again? (y/n):\n").lower().strip()
            if userSelection in ["yes", "y"]:
                return True
            elif userSelection in ["no", "n"]:
                exitCasino(self)
            else:
                errorHandler(self)

    def getPlayerStatistics(self, PlayerID=None):
        """
        Return the players statistics.
        """

        if PlayerID is None:
            PlayerID = self.PlayerID

        with open(self.filePath, "r") as file:
            allData = json.load(file)

        if PlayerID in allData:
            playerData = allData[PlayerID]
            print("\nPlayer Statistics")
            print(("_" * 17) + "\n")
            print(
                f"Player Name: {PlayerID}\n"
                f"Bankroll: {playerData['bankroll']:,}\n"
                f"Games Won: {playerData['gamesWon']}\n"
                f"Games Lost: {playerData['gamesLost']}\n"
                f"Win/Loss Ratio: {self.winLossRatio(playerData)}"
            )
            totalAmountWonLost = playerData["bankroll"] - 100000000
            if totalAmountWonLost > 0:
                print(f"Total Amount Won: {totalAmountWonLost:,} \n")
            elif totalAmountWonLost < 0:
                print(f"Total Amount Lost: {totalAmountWonLost:,} \n")

        while True:
            attemptExit = (
                input("Do you want to return to the main menu? (y/n):\n")
                .lower()
                .strip()
            )
            if attemptExit in ["yes", "y"]:
                break
            elif attemptExit in ["no", "n"]:
                exitCasino(self)
            else:
                errorHandler(self)

    def getPlayerName(self):
        """
        Prompt the user to enter their player name.
        """
        while True:
            name = input("Enter your player name: ").strip().title()
            if not name:
                errorHandler(self)
            elif len(name) > 10:
                print("Name must be less than 11 characters.")
            else:
                self.playerID = name
                return name

    def resetPlayerData(self):
        """
        Resets the specified players data back to default.

        100 million bankroll, 0 games won, 0 games lost.
        """

        while True:
            print("WARNING: This will reset your player data.")
            print("This action can't be undone.")
            userSelection = input("Do you want to continue? (y/n):\n").lower().strip()
            if userSelection in ["yes", "y"]:
                break
            elif userSelection in ["no", "n"]:
                exitCasino(self)
            else:
                errorHandler(self)

        with open(self.filePath, "r") as file:
            allData = json.load(file)
            allData[self.PlayerID] = {
                "playerName": self.PlayerID,
                "bankroll": 100000000,
                "gamesWon": 0,
                "gamesLost": 0,
            }
            self.savePlayerData(allData)
            print(f"Player {self.PlayerID}, data reset.")
            sleep(3)
            exit()
