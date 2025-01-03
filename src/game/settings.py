# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)

# Player settings
PLAYER_SPEED = 6
PLAYER_SIZE = 32
PLAYER_START_HEALTH = 200
PLAYER_START_MONEY = 100

# Player base stats
PLAYER_BASE_STATS = {
    "damage": 20,
    "attack_speed": 2.5,
    "crit_chance": 0.10,
    "crit_damage": 2.0,
    "move_speed": 6,
    "defense": 10,
    "attack_range": 150,
}

# Enemy settings
STARTING_ENEMIES = 4
ENEMY_SPAWN_RATE = 1.2
ENEMY_KILL_REWARD = 20
ENEMY_BASE_STATS = {
    "health": 60,
    "damage": 5,
    "speed": 3,
}

# Bonfire settings
BONFIRE_HEAL_AMOUNT = 75       # Increased healing amount
BONFIRE_HEAL_RADIUS = 48       # Increased activation radius
BONFIRE_COOLDOWN = 180         # Reduced cooldown to 3 seconds
BONFIRE_MIN_DISTANCE = 150     # Minimum distance between bonfires
BONFIRE_COUNT = 5              # Number of bonfires to spawn

# Shop settings
SHOP_REFRESH_COST = 20
SHOP_ITEMS_DISPLAYED = 4
SHOP_APPEAR_INTERVAL = 60

# Item rarity chances (in percentage)
ITEM_RARITY = {
    "COMMON": 50,
    "RARE": 30,
    "EPIC": 15,
    "LEGENDARY": 5
}

# Shader settings
SHADER_ENABLED = True
POST_PROCESSING = True 

# Round settings
ROUND_DURATION = 60 * FPS  # 1 minute per round (reduced from 3 minutes)
ROUND_BREAK_DURATION = 10 * FPS  # 10 seconds between rounds (reduced from 20)
STARTING_ROUND = 1
ENEMY_SCALING_PER_ROUND = 0.25  # Increased scaling to 25% per round for more intensity

# Shop settings
SHOP_REFRESH_COST = 20
SHOP_ITEMS_DISPLAYED = 4
SHOP_TIME_LIMIT = 15 * FPS  # 15 seconds to shop (reduced from 30)
ITEMS_PER_ROUND = 2  # Reduced from 3 to make choices more meaningful

# Game States
class GameStates:
    MENU = "menu"
    PLAYING = "playing"
    SHOPPING = "shopping"
    ROUND_TRANSITION = "round_transition"
    GAME_OVER = "game_over" 