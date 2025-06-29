

# Constants for the game
from enum import Enum


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Fighting Game"
LOCK_FPS = 60
GRAVITY = 2 * pow(LOCK_FPS, 2) # converted to per frame
CHARACTER_WIDTH = 60
CHARACTER_HEIGHT = 150
SHADOW_WIDTH = 80
SHADOW_HEIGHT = 15
MAIN_BACKGROUND = "assets/images/main_bg.png"
FONT= "assets/fonts/pixel.otf"
SOUND_BACKGROUND = "assets/sounds/sound_bg.mp3"

# Constants for networking

HOST = "localhost"
PORT = 8081

LITTLE_BYTE_ORDER = "little"  # Byte order for network packets
HEADER_SIZE = 8  # Size of the packet header in bytes

class CommandId(Enum):
    WAIT_FOR_MATCH = 1
    BROADCAST = 2
    MOVE = 3
    JUMP = 5
    ATK = 6
    END_GAME = 7

    

# Constants for scene management
MAIN_SCENE = "main"
BATTLE_SCENE = "battle"

# Colors
class Colors(Enum):
    RED = (255, 0, 0)
    BLACK = (0, 0, 0, 80)
    WHITE = (255, 255, 255)


# Constarts for characters
class CharacterId(Enum):
    ARCHER = 1
    FIGHTER = 2
    GORGON = 3
    VAMPIRE = 4
    WIZARD = 5
    TENGU = 6

class BackgroundId(Enum):
    BRIDGE = 1
    COUNTRY_SIDE = 2
    STREET = 3
    TEMPLE = 4
    TOKYO = 5


CHARACTER_STATES = {
    "idle": 0,
    "walk": 1,
    "jump": 2,
    "def": 3,
    "hit": 4,
    "atk_z": 5,
    "atk_x": 6,
    "atk_c": 7,
    "death": 8
}

CHARACTER_REVERSIBLE_STATES = {
    0: "idle",
    1: "walk",
    2: "jump",
    3: "def",
    4: "hit",
    5: "atk_z",
    6: "atk_x",
    7: "atk_c",
    8: "death"
}