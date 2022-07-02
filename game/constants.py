from string import ascii_lowercase, digits

SCREEN_LEFT = SCREEN_TOP = 0
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300

SCOREBOARD_FONT_SIZE = 25
SCOREBOARD_PADDING = (25, 15, 25, 15)
SCOREBOARD_PADDING_LEFT, SCOREBOARD_PADDING_TOP, SCOREBOARD_PADDING_RIGHT, SCOREBOARD_PADDING_BOTTOM = SCOREBOARD_PADDING

FONT_SIZE = 40
INTERFACE_SCALING = 1

CHARACTER_FADING_IN_DURATION = 1000
CHARACTER_DECAYING_DURATION = 3000
CHARACTER_FADING_OUT_DURATION = 50
CHARACTER_FADING_OUT_SCALE = 1.5

COLOR_BACKGROUND = (40, 40, 40)
COLOR_FONT = (150, 150, 200)
COLOR_FONT_DECAYING = (200, 100, 100)
COLOR_SCORE_FONT = (36, 255, 189)

LETTER_GROUPS = {
    "LOWERCASE": ascii_lowercase,
    "DIGITS": digits,
}
