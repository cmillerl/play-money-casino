import json
import os
from time import sleep


class House:
    def __init__(self, name="House"):

        self.name = name

        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.folderPath = os.path.join(self.directory, "json_data")
        self.filePath = os.path.join(self.folderPath, "house_data.json")

        # Default house data.
        self.data = {"name": self.name, "bankroll": 100000000000000}

        os.makedirs(self.folderPath, exist_ok=True)

        self.loadHouseData()

    def loadHouseData(self):
        """
        Load house data from a JSON file, if not found create a new one.
        """
        if os.path.exists(self.filePath):
            if os.path.getsize(self.filePath) == 0:
                self.saveHouseData()
            else:
                try:
                    with open(self.filePath, "r") as file:
                        self.data = json.load(file)
                except json.JSONDecodeError:
                    self.saveHouseData()
        else:
            self.saveHouseData()

    def saveHouseData(self):
        """
        Save house data to a JSON file.
        """
        with open(self.filePath, "w") as file:
            json.dump(self.data, file, indent=4)

    def displayHouseBankroll(self):
        """Print the houses current bankroll."""
        print(f"House bankroll: {self.data['bankroll']:,}")

    def resetHouseData(self):
        """
        Reset the house data to the default values.
        """
        self.data = {"name": self.name, "bankroll": 100000000000000}
        self.saveHouseData()
        print("House data has been reset...")
        sleep(3)
        exit()