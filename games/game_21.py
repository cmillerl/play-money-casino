from random import randint
from time import sleep
from utilities import errors, information, deck
import player
import house


class Game21:
    def __init__(self, player, house):

        # Game description
        self.gameDescription = """
Blackjack | 21:

Objective: 
Get a hand value closer to 21 than the dealer without exceeding 21.

Card Values:
- Number cards (2-10): Face value
- Face cards (J,Q,K): 10 points
- Ace: 1 or 11 points (whichever benefits you most)

Rules:
- Blackjack: A natural 21 with first two cards pays 2.5x bet
- Push: If tied with dealer, bet is returned
- Bust: If hand value exceeds 21, you lose
- Hit: Request another card
- Stand: Keep current hand
- Dealer must hit until hand value is 17 or higher
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

        # Copy of the standard deck of cards.
        self.standardDeckCopy = deck.standardDeck.copy()

        # For testing purposes only. To be removed.
        self.bet = 0

        # Initialize times hit for player and house to 0.
        self.timesHit = 0
        self.houseTimesHit = 0

        # Initialize player and house hands as an empty dictionary.
        self.playerHand = []
        self.houseHand = []

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

        print("Shuffling The Deck...")
        sleep(1)

        # Deal two cards to the player and the house.
        self.playerHand.append(self.drawCard(self.standardDeckCopy))
        self.playerScore += self.playerHand[0][1]
        self.houseHand.append(self.drawCard(self.standardDeckCopy))
        self.houseScore += self.houseHand[0][1]
        self.playerHand.append(self.drawCard(self.standardDeckCopy))
        self.playerScore += self.playerHand[1][1]
        self.houseHand.append(self.drawCard(self.standardDeckCopy))

        self.printPlayerHand()

        # Display the house hand with one card hidden.
        print("House hand: ", self.houseHand[0][0], "| Unknown card")
        print(f"House score: {self.houseScore}")
        sleep(1)

        # Set player turn to true and house turn to false.
        self.playerTurn = True
        self.houseTurn = False

        while self.playerTurn:
            if self.playerScore == 21 and self.timesHit == 0:
                print("Blackjack! You win 2.5x your bet!")
                self.player.data["bankroll"] += round(self.bet * 2.5, 0)
                self.player.data["gamesWon"] += 1
                self.house.data["bankroll"] -= round(self.bet * 2.5, 0)
                sleep(1)
                self.player.savePlayerData(self.player.data)
                self.player.displayPlayerBankroll()
                self.house.saveHouseData()
                if self.player.continuePlay():
                    self.resetGame()
            elif self.playerScore < 21:
                playerChoice = input("Hit or Stay: ").strip().lower()
                if playerChoice not in ["hit", "h", "s", "stay"]:
                    print("Invalid selection. Try again.")
                    continue
                elif playerChoice in ["hit", "h"]:
                    self.timesHit += 1
                    self.playerHand.append(self.drawCard(self.standardDeckCopy))
                    self.playerScore = 0
                    for card in self.playerHand:
                        self.playerScore += card[1]
                    self.printPlayerHand()
                    continue
                else:
                    self.playerTurn = False
                    self.houseTurn = True
                    break
            elif self.playerScore > 21:
                self.playerScore = self.containsAce(self.playerScore, self.playerHand)
                if self.playerScore > 21:
                    self.player.updatePlayerBankroll(won=False)
                    self.house.saveHouseData()
                    if self.player.continuePlay():
                        self.resetGame()
                else:
                    print(f"Your score: {self.playerScore}")
                    continue

        while self.houseTurn:
            print("Revealing houses hand...")
            sleep(1)
            self.houseScore += self.houseHand[1][1]
            self.printHouseHand()
            break
        if self.houseScore == 21 and self.houseTimesHit == 0:
            print("House has Blackjack!")
            self.player.updatePlayerBankroll(won=False)
            self.house.saveHouseData()
            if self.player.continuePlay():
                self.resetGame()
        while self.houseScore < 17:
            print("House hits...")
            self.houseTimesHit += 1
            sleep(1)
            self.houseHand.append(self.drawCard(self.standardDeckCopy))
            self.houseScore = 0
            for card in self.houseHand:
                self.houseScore += card[1]
            self.printHouseHand()

            if self.houseScore > 21:
                self.houseScore = self.containsAce(self.houseScore, self.houseHand)
                if self.houseScore > 21:
                    self.player.updatePlayerBankroll(won=True)
                    self.house.saveHouseData()
                    if self.player.continuePlay():
                        self.resetGame()
        if self.houseScore <= 21:
            if self.houseScore > self.playerScore:
                self.player.updatePlayerBankroll(won=False)
                self.house.saveHouseData()
                if self.player.continuePlay():
                    self.resetGame()
            elif self.houseScore < self.playerScore:
                self.player.updatePlayerBankroll(won=True)
                self.house.saveHouseData()
                if self.player.continuePlay():
                    self.resetGame()
            elif self.houseScore == self.playerScore:
                print("It's a tie!")
                sleep(1)
                print(
                    """
                      Push... 
                      Bet returned.
                      """) # fmt: skip
                sleep(1)
                self.player.displayPlayerBankroll()
                self.house.saveHouseData()
                if self.player.continuePlay():
                    self.resetGame()

    def drawCard(self, deck):
        """
        Draws a random card from the standard deck of cards.

        Removes the card from the deck and returns the card key and value.

        Can be used to draw a card for the player or the house.
        """
        deckKeys = list(deck.keys())
        cardKey = deckKeys[randint(0, len(deckKeys) - 1)]
        cardValue = deck.pop(cardKey)
        return (cardKey, cardValue)

    def containsAce(self, score, hand):
        """
        If the player or house score exceeds 21 and an Ace is in the hand

        the Ace value can be changed from 11 to 1 to prevent a bust.

        Returns the new score after changing the Ace value to 1.
        """
        if score <= 21:
            return score
        acesInDeck = sum(1 for card in hand if "Ace of " in card[0])
        while score > 21 and acesInDeck > 0:
            score -= 10
            acesInDeck -= 1
            if score <= 21:
                break
        return score

    def resetGame(self):
        """
        Resets the game to the starting state.

        Sets player and house scores to 0.

        Sets player and house hands to empty.

        Sets player turn to true and house turn to false.

        Clears the player hand and house hand.

        Resets the standard deck of cards.

        Starts a new game.
        """
        self.playerScore = 0
        self.houseScore = 0
        self.playerHand = []
        self.houseHand = []
        self.playerTurn = False
        self.houseTurn = False
        self.standardDeckCopy = deck.standardDeck.copy()
        self.gameStart()

    def printPlayerHand(self):
        """
        Print the players current hand and score.
        """
        for index, card in enumerate(self.playerHand):
            if index == 0:
                print("Your hand: ", card[0], end=" | ")
            elif index > 0 and index < len(self.playerHand) - 1:
                print(card[0], end=" | ")
            else:
                print(card[0], end="")
        print(f"\nYour score: {self.playerScore}")
        sleep(1)

    def printHouseHand(self):
        """
        Print the houses current hand and score.
        """
        for index, card in enumerate(self.houseHand):
            if index == 0:
                print("House hand: ", card[0], end=" | ")
            elif index > 0 and index < len(self.houseHand) - 1:
                print(card[0], end=" | ")
            else:
                print(card[0], end="")
        print(f"\nHouse score: {self.houseScore}")
        sleep(1)
