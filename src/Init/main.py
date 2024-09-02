from App.App import App
from States.Menu import Menu
from States.Game import Game
from States.LevelSelect import LevelSelect
from States.Results import Results

def main() -> None:
    Game = App()
    Game.run()

if __name__ == '__main__':
    main()
