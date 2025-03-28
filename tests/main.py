import unittest
import os
import sys

if __name__ == "__main__":
    # Add the current directory to sys.path to ensure board_game_sim can be imported
    current_dir = os.path.dirname(os.path.abspath(__file__))
    #os.chdir(os.path.abspath(os.path.join(current_dir, "..")))
    sys.path.insert(0, os.getcwd())
    sys.path.insert(1, os.path.abspath(os.path.join(current_dir, "..", "board_game_sim")))


    # Discover and run all tests in the tests directory
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=current_dir, pattern="test_*.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)
