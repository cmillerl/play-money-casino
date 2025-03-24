from random import randint
from time import sleep
from utilities import errors, information


class GameSlots:
    def __init__(self, player, house):

        # Game description
        self.gameDescription = """
╔══════════════════════════════╗
║           SLOTS              ║
╠══════════════════════════════╣
║    Match 3 symbols to win!   ║
║══════════════════════════════║
║    SYMBOL COLOR & PAYOUTS    ║
║══════════════════════════════║
║  White    = 2x    your bet   ║
║  Blue     = 3x    your bet   ║
║  Purple   = 5x    your bet   ║
║  Brown    = 8x    your bet   ║
║  Black    = 12x   your bet   ║
║  Red      = 25x   your bet   ║
║  $$$      = 600x your bet    ║
║══════════════════════════════║
║         Good luck!           ║
╚══════════════════════════════╝
        """ # fmt: skip

        # Initialize the house object.
        self.player = player
        self.house = house

        self.count = 0

        self.symbols = ["⬜", "🟦", "🟪", "🟫", "⬛", "🟥", "💲"]
        self.outcome = []
        self.spins = 0

    def gameStart(self):
        information.displayGameInformation(self)

        self.player.displayPlayerBankroll()
        self.player.getPlayerBet()
        sleep(1)

        try:
            self.spins = int(input("How many spins would you like to play?: "))
            if (self.spins * self.player.bet) > self.player.data["bankroll"]:
                print("You do not have enough money to play that many spins.")
                sleep(1)
                print("Spinning 1 time instead.")
                sleep(1)
                self.spins = 1
        except ValueError:
            errors.errorHandler()

        for i in range(self.spins):
            self.spinSlots()

        if self.player.continuePlay():
            self.resetGame()

    def spinSlots(self):
        """
        Spin the slots and determine the outcome.
        """
        self.outcome = []
        print("Spinning the slots...")
        sleep(1)
        for i in range(3):
            self.outcome.append(self.symbols[randint(0, len(self.symbols) - 1)])
            if i in [0, 1]:
                print(self.outcome[i], end=" | ")
            else:
                print(self.outcome[i])

        if self.outcome[0] == self.outcome[1] == self.outcome[2]:
            if self.outcome[0] == "💲":
                print("**********")
                print("JACKPOT!!!")
                print("**********")
                sleep(5)
            else:
                print("WINNER!")
                sleep(1)
                print("Calculating payout...")
                sleep(1)

            if self.outcome[0] == "⬜":
                self.winReward(amount=2)
            elif self.outcome[0] == "🟦":
                self.winReward(amount=3)
            elif self.outcome[0] == "🟪":
                self.winReward(amount=5)
            elif self.outcome[0] == "🟫":
                self.winReward(amount=8)
            elif self.outcome[0] == "⬛":
                self.winReward(amount=12)
            elif self.outcome[0] == "🟥":
                self.winReward(amount=25)
            elif self.outcome[0] == "💲":
                self.winReward(amount=600)
        else:
            self.player.updatePlayerBankroll(won=False)
            self.house.saveHouseData()

    def resetGame(self):
        """
        Resets the game to the starting state.

        Starts a new game.
        """
        self.outcome = []
        self.gameStart()

    def winReward(self, amount):
        """
        Handles the reward payout when a player wins on the slot machine.

        Arguments: amount (int): The multiplier for the bet amount.

        Updates:
            - Player's bankroll with winnings
            - Player's games won count
            - House bankroll
            - Saves updated data for both player and house
            - Displays updated bankroll to player
        """
        self.totalWin = amount * self.player.bet
        print(f"You won {self.totalWin:,}!")
        sleep(3)
        self.player.data["bankroll"] += self.totalWin
        self.player.data["gamesWon"] += 1
        self.house.data["bankroll"] -= self.totalWin
        self.player.savePlayerData(self.player.data)
        self.player.displayPlayerBankroll()
        self.house.saveHouseData()
        sleep(3)
