### type-with-songs

Simple game in pygame where you type all the letters that appear on the screen.

#### Install

Clone repo and install [pygame](https://www.pygame.org/wiki/GettingStarted).

#### Usage

Run `main.py <level_filename>` where `level_filename` is name of the level file in side `/data` directory (i.e. `first.yaml`, `random.yaml`)

Change game parameters by fiddling in `constants.py` file.

#### TODO

* ~~add pytest and do lots of more tests~~ create more tests
* scoreboard on top of the screen with information: hits/misses, time left
* add support for lowercase/uppercase and symbols that need shift modifier
* add music in background
* ~~create map files which will determine when what letters appear~~
* add menu where you can select map
* add map editor, so it's possible to sync appearing letters with music
* some kind of graphic overhaul, so it doesn't look so ugly
* add infinite mode where new letter will appear after the previous one gets "hit"
