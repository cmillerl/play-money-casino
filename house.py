class House:
    def __init__(self):

        # Initial house bankroll set to 100 trillion.
        self.bankroll = 100000000000000

    def displayHouseBankroll(self):
        """Print the houses current bankroll."""
        print(f"House bankroll: {self.bankroll:,}")
