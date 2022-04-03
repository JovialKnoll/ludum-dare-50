import sys
import os


TITLE = "Ready, uNsTeAdY, FIRE!"
SCREEN_SIZE = (640, 360)
COLORKEY = (255, 0, 255)
FONT_SIZE = 24
FONT_HEIGHT = 28
FONT_ANTIALIAS = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ENEMY_COLOR0 = (35, 35, 97)
ENEMY_COLOR1 = (155, 174, 181)

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
WINDOW_ICON = os.path.join(GRAPHICS_DIRECTORY, 'icon.png')
FONT = os.path.join(GRAPHICS_DIRECTORY, 'Roboto-Regular.ttf')

TITLE_FONT = os.path.join(GRAPHICS_DIRECTORY, 'Roboto-Black.ttf')

LOGOS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'logos')
JK_LOGO_BLACK = os.path.join(LOGOS_DIRECTORY, 'jklogo.png')

SPRITES_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'sprites')
SHIP = os.path.join(SPRITES_DIRECTORY, 'ship.png')
SHIP_MASK = os.path.join(SPRITES_DIRECTORY, 'ship_mask.png')
ENEMY0 = os.path.join(SPRITES_DIRECTORY, 'enemy0.png')
ENEMY1 = os.path.join(SPRITES_DIRECTORY, 'enemy1.png')
ENEMY2 = os.path.join(SPRITES_DIRECTORY, 'enemy2.png')

RAO = os.path.join(SOUND_DIRECTORY, 'rao.ogg')
BWOM = os.path.join(SOUND_DIRECTORY, 'bwom.ogg')
EXPLODE = os.path.join(SOUND_DIRECTORY, 'explode.ogg')
TITLE_SOUND = os.path.join(SOUND_DIRECTORY, 'title.ogg')
JOVIAL_SOUND = os.path.join(SOUND_DIRECTORY, 'jovial.ogg')

MUSIC_DIRECTORY = os.path.join(SOUND_DIRECTORY, 'music')
MUSIC0 = os.path.join(MUSIC_DIRECTORY, 'music0.ogg')
MUSIC1 = os.path.join(MUSIC_DIRECTORY, 'music1.ogg')
MUSIC2 = os.path.join(MUSIC_DIRECTORY, 'music2.ogg')

VERSION_TEXT = os.path.join(TEXT_DIRECTORY, 'version.txt')

VERSION = ''
try:
    with open(VERSION_TEXT) as version_file:
        VERSION = version_file.readline().rstrip('\n')
except FileNotFoundError:
    pass
