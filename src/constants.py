import sys
import os


TITLE = "GAME_NAME_HERE"
SCREEN_SIZE = (640, 360)
COLORKEY = (255, 0, 255)
FONT_SIZE = 24
FONT_HEIGHT = 28
FONT_ANTIALIAS = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

_location = '.'
if getattr(sys, 'frozen', False):
    _location = sys.executable
elif __file__:
    _location = __file__
SRC_DIRECTORY = os.path.dirname(_location)

ASSETS_DIRECTORY = os.path.join(SRC_DIRECTORY, 'assets')
GRAPHICS_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'gfx')
SOUND_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'sfx')
TEXT_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'txt')
SAVE_DIRECTORY = os.path.join(SRC_DIRECTORY, 'saves')
SCREENSHOT_DIRECTORY = os.path.join(SRC_DIRECTORY, 'screenshots')

CONFIG_FILE = os.path.join(SRC_DIRECTORY, 'config.ini')
WINDOW_ICON = None#os.path.join(GRAPHICS_DIRECTORY, 'icon.png')
FONT = os.path.join(GRAPHICS_DIRECTORY, 'Roboto-Regular.ttf')

TITLE_FONT = os.path.join(GRAPHICS_DIRECTORY, 'Roboto-Black.ttf')

LOGOS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'logos')
JK_LOGO_BLACK = os.path.join(LOGOS_DIRECTORY, 'jklogo.png')

MUSIC_DIRECTORY = os.path.join(SOUND_DIRECTORY, 'music')

VERSION_TEXT = os.path.join(TEXT_DIRECTORY, 'version.txt')
CREDITS_TEXT = os.path.join(TEXT_DIRECTORY, 'credits.txt')

VERSION = ''
try:
    with open(VERSION_TEXT) as version_file:
        VERSION = version_file.readline().rstrip('\n')
except FileNotFoundError:
    pass
