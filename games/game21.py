from random import randint
from time import sleep
from utilities import errors, information, deck
import player
import house


class Game21:
    def __init__(self):

        self.A = 'A'

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

        self.copiedDeck = deck.standardDeck.copy()

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

        print("You will go first after the house shuffles the deck.")
        sleep(1)
        print("Shuffling...")
        sleep(1)

        playerHand = []
        houseHand = []

        for _ in range(2):
            playerHand.append(self.copiedDeck.pop(randint(0, len(self.copiedDeck) - 1)))
            houseHand.append(self.copiedDeck.pop(randint(0, len(self.copiedDeck) - 1)))
        
        playerHand = self.handContainsAce(playerHand)
        houseHand = self.handContainsAce(houseHand)
    
        print(f"Your hand: {playerHand}")
        print(f"Dealer's visible card: {houseHand[0]}")
    
        return playerHand, houseHand    
    
    def handContainsAce(self, hand):
        return [self.A if card in [1, 11] else card for card in hand]