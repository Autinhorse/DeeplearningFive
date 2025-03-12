import logging
import sys

from GameCheckers.Checkers import Checkers
from GameFive.Five import Five


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

if __name__ == '__main__':
    # game = Five()
    game = Checkers()
    game.StartGame()
