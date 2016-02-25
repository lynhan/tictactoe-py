# run.py

"""
Get user input and start game.
"""

from game import TicTacToe

def main():

    game = TicTacToe()
    game.start()

    while not game.over:
        game.turn()

if __name__ == "__main__":
    main();
