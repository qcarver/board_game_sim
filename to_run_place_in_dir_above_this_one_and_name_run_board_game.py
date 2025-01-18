# filepath: /home/qcarver/Documents/NightTrain/run_board_game.py
import os
import sys

# Append the relative path to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'board_game_sim'))

from board_game_sim import Game

if __name__ == "__main__":
    game = Game()
    game.run_game()
