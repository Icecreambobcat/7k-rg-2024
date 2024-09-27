# 4k-rg-2024

A 4k rhythm game built in python for school

## Dependancies

- [Python 3.12](https://www.python.org/downloads/)
- [Pygame 2.1.0](https://www.pygame.org/wiki/GettingStarted)

### Python dependancies

- pathlib
  - `pip3 install pathlib`

## How to run

- It's suggested that you run the game in a venv
  - `pip3 install venv`
    - `python3 -m venv venv`

```zsh
cd <PROJECT_DIRECTORY>
source venv/bin/activate
python3 -m src.Init.main
```

- It's also suggested that you occasionally pull the repo if there are updates

### What to do ingame

- Menu instructions are self explanatory
- the keymap follows that of a standard 7k rhythm game: s, d, f, space, j, k, l
- Hold notes should be released as their bodies finish crossing the line
- Custom maps can be imported into the game by unzipping a `.osz` file and moving the directory into the `Levels` folder
  - It's recommended that you don't have more than 10 difficulties installed at any given time
  
## CUSTOM FEATURES

- High extensibility with custom imports (this counts as quite a few)
  - Can read typical `.osu` format level files
  - Extremely high room for expansion with full parsing of the files
  - Auto parsing and loading of level assets
  - Levels are loaded into memory at the start of gameplay
- Literally a rhythm game
  - Do I really need to tell you what a rhythm game is?
  - Temporary score saving
