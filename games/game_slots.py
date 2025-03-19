from random import randint
from time import sleep
from utilities import errors, information
import player
import house


class GameSlots:
    def __init__(self, player, house):

        # Game description
        self.gameDescription = """
Slots:

Match 3 symbols to win! Different symbols have different payouts:

🟥 - 3x your bet
🟧 - 4x your bet
🟨 - 5x your bet
🟩 - 6x your bet
🟦 - 7x your bet
🟪 - 8x your bet
💲 - JACKPOT! 1000x your bet!

Good luck!
        """

        # Initialize the house object.
        self.player = player
        self.house = house

        self.count = 0

        self.symbols = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪", "💲"]
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

            if self.outcome[0] == "🟥":
                print(f"Your payout is: {self.player.bet * 3}")
                self.player.data["bankroll"] += self.player.bet * 3
                self.player.data["gamesWon"] += 1
                self.house.data["bankroll"] -= self.player.bet * 3
                self.player.savePlayerData(self.player.data)
                self.player.displayPlayerBankroll()
                self.house.saveHouseData()
                sleep(5)
            elif self.outcome[0] == "🟧":
                print(f"Your payout is: {self.player.bet * 4}")
                self.player.data["bankroll"] += self.player.bet * 4
                self.player.data["gamesWon"] += 1
                self.house.data["bankroll"] -= self.player.bet * 4
                self.player.savePlayerData(self.player.data)
                self.player.displayPlayerBankroll()
                self.house.saveHouseData()
                sleep(5)
            elif self.outcome[0] == "🟨":
                print(f"Your payout is: {self.player.bet * 5}")
                self.player.data["bankroll"] += self.player.bet * 5
                self.player.data["gamesWon"] += 1
                self.house.data["bankroll"] -= self.player.bet * 5
                self.player.savePlayerData(self.player.data)
                self.player.displayPlayerBankroll()
                self.house.saveHouseData()
                sleep(5)
            elif self.outcome[0] == "🟩":
                print(f"Your payout is: {self.player.bet * 6}")
                self.player.data["bankroll"] += self.player.bet * 6
                self.player.data["gamesWon"] += 1
                self.house.data["bankroll"] -= self.player.bet * 6
                self.player.savePlayerData(self.player.data)
                self.player.displayPlayerBankroll()
                self.house.saveHouseData()
                sleep(5)
            elif self.outcome[0] == "🟦":
                print(f"Your payout is: {self.player.bet * 7}")
                self.player.data["bankroll"] += self.player.bet * 7
                self.player.data["gamesWon"] += 1
                self.house.data["bankroll"] -= self.player.bet * 7
                self.player.savePlayerData(self.player.data)
                self.player.displayPlayerBankroll()
                self.house.saveHouseData()
                sleep(5)
            elif self.outcome[0] == "🟪":
                print(f"Your payout is: {self.player.bet * 8}")
                self.player.data["bankroll"] += self.player.bet * 8
                self.player.data["gamesWon"] += 1
                self.house.data["bankroll"] -= self.player.bet * 8
                self.player.savePlayerData(self.player.data)
                self.player.displayPlayerBankroll()
                self.house.saveHouseData()
                sleep(5)
            elif self.outcome[0] == "💲":
                print(f"Your payout is: {self.player.bet * 1000}")
                self.player.data["bankroll"] += self.player.bet * 1000
                self.player.data["gamesWon"] += 1
                self.house.data["bankroll"] -= self.player.bet * 1000
                self.player.savePlayerData(self.player.data)
                self.player.displayPlayerBankroll()
                self.house.saveHouseData()
                sleep(5)
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
