# 4k-rg-2024

A 4k rhythm game built in python for school

## Dependancies

- [Python 3.12](https://www.python.org/downloads/)
- [Pygame 2.1.0](https://www.pygame.org/wiki/GettingStarted)

### Python dependancies

- pathlib
  - `pip3 install pathlib`

## How to run

- MANDATORY:
  - YOUR SCREEN MUST BE AT LEAST 1920x1080
  - You can turn up your resolution in your system settings temporarily for this game
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
  - Custom imports should be 7k charts
- As usual... if something breaks, try relaunching the game a few times first
  
## CUSTOM FEATURES

- High extensibility with custom imports (this counts as quite a few)
  - Can read typical `.osu` format level files
  - Extremely high room for expansion with full parsing of the files
  - Auto parsing and loading of level assets
  - Levels are loaded into memory at the start of gameplay
  - To load extra maps:
    - Unzip a `.osz` file
    - rename the directory to the name of the song as seen on `osu.ppy.sh`
    - move it into `Levels`
    - go to the main menu and then back to the level select
    - the song should be right there!
- Literally a rhythm game
  - Do I really need to tell you what a rhythm game is?
  - Temporary score saving
