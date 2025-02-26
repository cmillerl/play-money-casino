from random import randint
from time import sleep
import player
import house


class ClosestToOneHundred:
    def __init__(self):

        # Game description
        self.gameDescription = """
The objective of the game is to get as close to 100 as possible without going over.
You will go first and continue until they want to stop rolling the dice.
If your rolls don't exceed 100, the house will then roll the dice.
The house will continue to roll until it gets a score that is greater than or equal to yours.
You wins if the house goes over 100.
The house wins if the house gets a score closer to 100 than you.
        """

        # Initialize the player and house objects.
        self.player = player.Player()
        self.house = house.House()

        # Scores for the player and the house set to 0.
        self.houseScore = 0
        self.playerScore = 0

        # Boolean values to determine whose turn it is.
        self.houseTurn = False
        self.playerTurn = False

        # The possible values from one roll of the dice.
        self.diceRollScore = randint(1, 100)

        self.count = 0

    def gameStart(self):
        while self.count < 1:
            userSelection = (input("Do you want to read the games description?\n")).lower().strip()  # fmt: skip
            self.count += 1
            if userSelection in ["yes", "y"]:
                print(self.gameDescription)
            elif userSelection in ["no", "n"]:
                print("Okay, let's start the game.")
                break
            else:
                print("Invalid input. Please enter yes or no.")
                sleep(1)
                self.count = 0
                self.gameStart()

            while True:
                userSelection = input("Do you want to start the game?\n").lower().strip()  # fmt: skip
                if userSelection in ["yes", "y"]:
                    break
                elif userSelection in ["no", "n"]:
                    print("Okay, goodbye!")
                    exit()
                else:
                    print("Invalid input. Please enter yes or no.")
                    sleep(1)

        print("The game will now begin.")
        sleep(1)
        self.player.displayPlayerBankroll()
        sleep(1)
        self.house.displayHouseBankroll()
        sleep(1)

        self.player.getPlayerBet()
        sleep(1)

        print("You will go first.")
        sleep(1)
        self.playerTurn = True
        print("You will now roll the dice.")
        sleep(1)

        while self.playerTurn:
            self.diceRollScore = randint(1, 100)
            print(f"You rolled a {self.diceRollScore}.")
            self.playerScore += self.diceRollScore
            print(f"Your score: {self.playerScore}")
            if self.playerScore == 100:
                self.player.gamesWon += 1
                sleep(1)
                print("Congratulations! You win!")
                self.player.updatePlayerBankroll(won=True)
                self.house.data["bankroll"] -= self.player.bet
                self.house.saveHouseData()
                print(f"Your bankroll: {self.player.data["bankroll"]:,}")
                if self.player.continuePlay():
                    self.playerScore = 0
                    self.houseScore = 0
                    self.playerTurn = True
                    self.houseTurn = False
                    self.gameStart()
            elif self.playerScore > 100:
                self.player.data["gamesLost"] += 1
                sleep(1)
                print("You lose.")
                self.player.updatePlayerBankroll(won=False)
                self.house.data["bankroll"] += self.player.bet
                self.house.saveHouseData()
                print(f"Your bankroll: {self.player.data["bankroll"]:,}")
                if self.player.continuePlay():
                    self.playerScore = 0
                    self.houseScore = 0
                    self.playerTurn = True
                    self.houseTurn = False
                    self.gameStart()
            else:
                userSelection = (input("Do you want to roll the dice again?\n").lower().strip())  # fmt: skip
                if userSelection not in ["yes", "y"]:
                    self.playerTurn = False
                    self.houseTurn = True

        print("The house will now roll the dice.")
        sleep(1)
        while self.houseTurn:
            self.diceRollScore = randint(1, 100)
            print(f"The house rolled a {self.diceRollScore}.")
            sleep(1)
            self.houseScore += self.diceRollScore
            print(f"House score: {self.houseScore}")
            if self.houseScore > 100:
                self.player.data["gamesWon"] += 1
                sleep(1)
                print("Congratulations! The house went over 100. You win!")
                self.player.updatePlayerBankroll(won=True)
                self.house.data["bankroll"] -= self.player.bet
                self.house.saveHouseData()
                self.houseTurn = False
                print(f"Your bankroll: {self.player.data["bankroll"]:,}")
                if self.player.continuePlay():
                    self.playerScore = 0
                    self.houseScore = 0
                    self.playerTurn = True
                    self.houseTurn = False
                    self.gameStart()
            elif self.houseScore > self.playerScore:
                self.player.data["gamesLost"] += 1
                sleep(1)
                print("The house wins.")
                self.player.updatePlayerBankroll(won=False)
                self.house.data["bankroll"] += self.player.bet
                self.house.saveHouseData()
                print(f"Your bankroll: {self.player.data["bankroll"]:,}")
                self.houseTurn = False
                if self.player.continuePlay():
                    self.playerScore = 0
                    self.houseScore = 0
                    self.playerTurn = True
                    self.houseTurn = False
                    self.gameStart()
            elif self.houseScore == self.playerScore:
                sleep(1)
                print("You win!")
                self.player.data["gamesWon"] += 1
                self.player.updatePlayerBankroll(won=True)
                self.house.data["bankroll"] -= self.player.bet
                self.house.saveHouseData()
                print(f"Your bankroll: {self.player.data["bankroll"]:,}")
                self.houseTurn = False
                if self.player.continuePlay():
                    self.playerScore = 0
                    self.houseScore = 0
                    self.playerTurn = True
                    self.houseTurn = False
                    self.gameStart()
            else:
                print("The house will roll again.")
                sleep(1)
