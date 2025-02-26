import logging
from time import sleep

# This module contains error functions. They aren't considered methods because they aren't tied to a class.

logging.basicConfig(
    level=logging.ERROR,
    format="%(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


def errorHandler():
    logging.error("An error occurred with your input.")
    sleep(1)
    print("Trying again...")
    sleep(1)
