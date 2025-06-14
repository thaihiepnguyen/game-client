


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

# Constants for scene management
MAIN_MENU_SCENE = "main_menu"
LOGIN_SCENE = "login"
BATTLE_SCENE = "battle"

# Constants for animations
ATTACK_COOLDOWN = 500

# Colors
class Colors(Enum):
    RED = (255, 0, 0)
    BLACK = (0, 0, 0, 80)