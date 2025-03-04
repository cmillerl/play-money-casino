from random import randint
from time import sleep
from utilities import errors, information
import player
import house


class Game100:
    def __init__(self):

        # Game description
        self.gameDescription = """
100:

Objective:
Get a score as close to 100 as possible without going over.

Rules:
You will roll first, getting a random number between 1-100 each roll.
You can roll as many times as you want, adding to your total score.
If you go over 100, you lose immediately.
If you decide to stop, the house will then roll.

The house must keep rolling until it either:
- Beats your score.
- Ties your score.
- Rolls over 100.

You win if the house ties your score or rolls over 100.
You lose if the house beats your score.
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

        self.count = 0

    def gameStart(self):
        information.displayGameInformation(self)

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
            # The possible values from one roll of the dice.
            self.diceRollScore = randint(1, 100)
            print(f"You rolled a {self.diceRollScore}.")
            self.playerScore += self.diceRollScore
            print(f"Your score: {self.playerScore}")
            if self.playerScore == 100:
                sleep(1)
                self.player.updatePlayerBankroll(won=True)
                self.house.saveHouseData()
                if self.player.continuePlay():
                    self.resetGame()
            elif self.playerScore > 100:
                sleep(1)
                self.player.updatePlayerBankroll(won=False)
                self.house.saveHouseData()
                if self.player.continuePlay():
                    self.resetGame()
            else:
                while True:
                    userSelection = (input("Do you want to roll the dice again?\n").lower().strip())  # fmt: skip
                    if userSelection in ["yes", "y"]:
                        print("You will roll again.")
                        sleep(1)
                        break
                    elif userSelection in ["no", "n"]:
                        print("Your turn is over.")
                        sleep(1)
                        self.playerTurn = False
                        self.houseTurn = True
                        break
                    else:
                        errors.errorHandler()

        print("The house will now roll the dice.")
        sleep(1)
        while self.houseTurn:
            self.diceRollScore = randint(1, 100)
            print(f"The house rolled a {self.diceRollScore}.")
            sleep(1)
            self.houseScore += self.diceRollScore
            print(f"House score: {self.houseScore}")
            if self.houseScore > 100:
                sleep(1)
                self.player.updatePlayerBankroll(won=True)
                self.house.saveHouseData()
                self.houseTurn = False
                if self.player.continuePlay():
                    self.resetGame()
            elif self.houseScore > self.playerScore:
                sleep(1)
                self.player.updatePlayerBankroll(won=False)
                self.house.saveHouseData()
                self.houseTurn = False
                if self.player.continuePlay():
                    self.resetGame()
            elif self.houseScore == self.playerScore:
                sleep(1)
                self.player.updatePlayerBankroll(won=True)
                self.house.saveHouseData()
                self.houseTurn = False
                if self.player.continuePlay():
                    self.resetGame()
            else:
                print("The house will roll again.")
                sleep(1)

    def resetGame(self):
        """
        Resets the game to the starting state.

        Sets player and house scores to 0.

        Sets player turn to true and house turn to false.

        Starts a new game.
        """
        self.playerScore = 0
        self.houseScore = 0
        self.playerTurn = False
        self.houseTurn = False
        self.gameStart()
