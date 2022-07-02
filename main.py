import sys
from game.game import Game

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <level_filename>")
        sys.exit(1)
    game = Game(sys.argv[1])
    game.run_main_loop()
