# Mercury Rails Game: A text-based game of resource management and strategy on Mercury.
# The author qcarver@gmail.com does NOT authorize the use of this code for ANYTHING 
# it is the intellectual property of the Carver family and shouldn't be destributed. 
# Even worse, it is a work in progress and not ready for ANYONE ANYWAY. Good Talk! 

# filepath: /home/qcarver/Documents/NightTrain/board_game_sim/__init__.py
from .resources import ResourceType, Resources
from .player import Player
from .cards import Card, CardDeck
from .game import Game

if __name__ == "__main__":
    game = Game()
    game.run_game()