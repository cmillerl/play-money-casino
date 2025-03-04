from random import randint
from time import sleep
from utilities import errors, information, deck
import player
import house


class Game21:
    def __init__(self):

        # Game description
        self.gameDescription = """
TBD
Blackjack
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

        self.standardDeckCopy = deck.standardDeck.copy()

        self.count = 0

        self.bet = 0

    def gameStart(self):
        # information.displayGameInformation(self)

        # print("The game will now begin.")
        # sleep(1)
        # self.player.displayPlayerBankroll()
        # sleep(1)
        # self.house.displayHouseBankroll()
        # sleep(1)

        # self.player.getPlayerBet()
        # sleep(1)

        print("You will go first after the house shuffles the deck.")
        sleep(1)
        print("Shuffling...")
        sleep(1)

        playerHand = []
        houseHand = []

        playerHand.append(self.drawCard(self.standardDeckCopy))
        self.playerScore += playerHand[0][1]
        houseHand.append(self.drawCard(self.standardDeckCopy))
        self.houseScore += houseHand[0][1]
        playerHand.append(self.drawCard(self.standardDeckCopy))
        self.playerScore += playerHand[1][1]
        houseHand.append(self.drawCard(self.standardDeckCopy))

        print("Your hand: ", playerHand[0][0], " | ", playerHand[1][0])
        print(f"Your score: {self.playerScore}")
        sleep(1)
        print("House hand: ", houseHand[0][0], "| Unknown card")
        print(f"House score: {self.houseScore}")
        sleep(1)

        self.playerTurn = True
        self.houseTurn = False

        while self.playerTurn:
            i = 2
            if self.playerScore == 21:
                print("Blackjack! You win 2.5x your bet!")
                self.player.data["bankroll"] += self.bet * 2.5
                self.player.data["gamesWon"] += 1
                self.house.data["bankroll"] -= self.bet * 2.5
                sleep(1)
                self.player.displayPlayerBankroll()
                self.house.saveHouseData()
                if self.player.continuePlay():
                    self.resetGame()
                break
            elif self.playerScore > 21:
                self.containsAce(self.playerScore, playerHand)
                self.player.updatePlayerBankroll(won=False)
                self.house.saveHouseData()
                if self.player.continuePlay():
                    self.resetGame()
                break
            elif self.playerScore < 21:
                playerChoice = input("Hit or Stay: ").strip().lower()
                if playerChoice not in ["hit", "h", "s", "stay"]:
                    print("Invalid selection. Try again.")
                    continue
                elif playerChoice in ["hit", "h"]:
                    playerHand.append(self.drawCard(self.standardDeckCopy))
                    self.playerScore += playerHand[2][1]
                    print("Your hand: ", playerHand[0][0], " | ", playerHand[1][0], " | ", playerHand[i][0])
                    print(f"Your score: {self.playerScore}")
                    i += 1
                    sleep(1)
                    continue
                else:
                    self.playerTurn = False
                    self.houseTurn = True
                    break

        while self.houseTurn:
            i = 2
            print("Revealing houses hand...")
            sleep(1)
            print("Houses hand: ", houseHand[0][0], " | ", houseHand[1][0])
            self.houseScore += houseHand[1][1]
            sleep(1)
            print(f"House score: {self.houseScore}")
            break

        if self.houseScore == 21:
            print("House has Blackjack!")
            self.player.updatePlayerBankroll(won=False)
            self.house.saveHouseData()
            if self.player.continuePlay():
                self.resetGame()
        elif self.houseScore < 17:
            while self.houseScore < 17:
                print("House hits...")
                sleep(1)
                houseHand.append(self.drawCard(self.standardDeckCopy))
                self.houseScore += houseHand[i][1]
                print("House hand: ", houseHand[0][0], "| ", houseHand[1][0], "| ", houseHand[i][0])
                i += 1
                sleep(1)
                print(f"House score: {self.houseScore}")
                sleep(1)
            if self.houseScore > 21:
                self.containsAce(self.houseScore, houseHand)
                self.player.updatePlayerBankroll(won=True)
                self.house.saveHouseData()
                if self.player.continuePlay():
                    self.resetGame()
        elif self.houseScore > self.playerScore:
            self.player.updatePlayerBankroll(won=False)
            self.house.saveHouseData()
            if self.player.continuePlay():
                self.resetGame()
        elif self.houseScore < self.playerScore:
            self.player.updatePlayerBankroll(won=True)
            self.house.saveHouseData()
            if self.player.continuePlay():
                self.resetGame()

    def drawCard(self, deck):
        deckKeys = list(deck.keys())
        cardKey = deckKeys[randint(0, len(deckKeys) - 1)]
        cardValue = deck.pop(cardKey)
        return (cardKey, cardValue)

    def containsAce(self, score, hand):
        if score > 21:
            for card in hand:
                if "Ace" in card[0]:
                    score -= 10
                    return score
            return score
        else:
            return score
        
    def resetGame(self):
        """
        Resets the game to the starting state.

        Sets player and house scores to 0.

        Sets player and house hands to empty.

        Sets player turn to true and house turn to false.

        Starts a new game.
        """
        self.playerScore = 0
        self.houseScore = 0
        self.playerHand = []
        self.houseHand = []
        self.playerTurn = False
        self.houseTurn = False
        self.gameStart()
