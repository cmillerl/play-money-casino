from random import randint
from time import sleep
from utilities import errors, information
import player
import house


class Game100To0:
    def __init__(self, player, house):

        # Game description
        self.gameDescription = """
100 to 0:

Objective:
- Start with 100 points and be the first to reach exactly 0 points.
- Both players share the same pool of points.

Rules:
- Players take turns rolling a dice with a range from 0 to the number of points left.
- You roll first, and your roll amount is subtracted from points left.
- The house then rolls, and its roll is subtracted from points left.
- Turns alternate until someone reaches exactly 0.

Special Case - When at 1 point:
- You must roll exactly 1 to win.
- Both you and the house have a 50% chance of rolling 0 (no change) and 50% chance of rolling 1.

Winning/Losing:
- You win if you reach 0 before the house.
- You lose if the house reaches 0 before you.
        """

        # Initialize the house object.
        self.player = player
        self.house = house

        # Scores for the player and the house set to 0.
        self.houseScore = 0
        self.playerScore = 0

        # Boolean values to determine whose turn it is.
        self.houseTurn = False
        self.playerTurn = False

        self.totalPoints = 100

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

        while self.totalPoints > 0:
            if self.playerTurn:
                self.rollDice()
                if self.totalPoints == 0:
                    self.player.updatePlayerBankroll(won=True)
                    self.house.saveHouseData()
                    if self.player.continuePlay():
                        self.resetGame()
                        break
                self.playerTurn = False
                self.houseTurn = True
            elif self.houseTurn:
                self.rollDice()
                if self.totalPoints == 0:
                    self.player.updatePlayerBankroll(won=False)
                    self.house.saveHouseData()
                    if self.player.continuePlay():
                        self.resetGame()
                        break
                self.houseTurn = False
                self.playerTurn = True

    def rollDice(self):
        """
        This method will roll the dice for the player and the house.

        Rolls the dice with values from 0 to the total points left.

        If there's only 1 point left, the player must roll exactly 1 to win with a 50% chance of rolling 0.
        """

        if self.totalPoints > 1:
            diceRoll = randint(1, self.totalPoints)
            self.totalPoints -= diceRoll
            sleep(1)
            if self.playerTurn:
                print(f"You rolled a {diceRoll}.")
                sleep(1)
                print(f"Points remaining: {self.totalPoints}")
                sleep(1)
            elif self.houseTurn:
                print(f"The house rolled a {diceRoll}.")
                sleep(1)
                print(f"Points remaining: {self.totalPoints}")
        else:
            diceRoll = randint(0, 1)
            self.totalPoints -= diceRoll
            sleep(1)
            if self.playerTurn:
                print(f"You rolled a {diceRoll}.")
                sleep(1)
                print(f"Points remaining: {self.totalPoints}")
                sleep(1)
            elif self.houseTurn:
                print(f"The house rolled a {diceRoll}.")
                sleep(1)
                print(f"Points remaining: {self.totalPoints}")
                sleep(1)

    def resetGame(self):
        """
        Resets the game to the starting state.

        Sets the total points to 100.

        Sets player turn to true and house turn to false.

        Starts a new game.
        """
        self.totalPoints = 100
        self.playerTurn = False
        self.houseTurn = False
        self.gameStart()
