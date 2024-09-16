from ..App.App import App
from sys import exit
import argparse as ap

def main() -> None:
    Game = App()
    Game.run()
    # potentially use launch flags/args IE:
    # parser = ap.ArgumentParser()
    # args = parser.parse_args()

if __name__ == "__main__":
    main()
