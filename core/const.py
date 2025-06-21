

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

# Constants for scene management
MAIN_MENU_SCENE = "main_menu"
MAIN_SCENE = "main"
BATTLE_SCENE = "battle"

# Constants for animations
ATTACK_COOLDOWN = 500

# Colors
class Colors(Enum):
    RED = (255, 0, 0)
    BLACK = (0, 0, 0, 80)