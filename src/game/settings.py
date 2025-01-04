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
STARTING_ENEMIES = 3
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
ENEMY_SCALING_PER_ROUND = 0.25  # Base stat increase per round
ENEMY_COUNT_INCREASE = 1  # How many additional enemies per round
ENEMY_SPAWN_DELAY = FPS * 3  # Delay between enemy spawns
MAX_ENEMIES = 15  # Maximum enemies allowed at once

# Shop settings
SHOP_REFRESH_COST = 20
SHOP_ITEMS_DISPLAYED = 4
SHOP_TIME_LIMIT = 15 * FPS  # 15 seconds to shop (reduced from 30)
ITEMS_PER_ROUND = 2  # Reduced from 3 to make choices more meaningful

# Progressive Difficulty Modifiers
SPEED_SCALING = 0.1  # Enemy speed increases by 10% per round
HEALTH_SCALING = 0.2  # Enemy health increases by 20% per round
DAMAGE_SCALING = 0.15  # Enemy damage increases by 15% per round
SPAWN_RATE_DECREASE = 0.95  # Spawn delay decreases by 5% per round (faster spawns)

# Round Rewards
BASE_ROUND_REWARD = 50  # Base money reward for completing a round
REWARD_SCALING = 0.3  # Reward increases by 30% per round

# Enemy Tiers
ENEMY_TIERS = {
    "BASIC": {
        "health": 40,
        "damage": 3,
        "speed": 2,
        "color": (150, 150, 150),  # Light gray
        "reward": 15
    },
    "STANDARD": {
        "health": 60,
        "damage": 5,
        "speed": 3,
        "color": (200, 100, 100),  # Light red
        "reward": 20
    },
    "ADVANCED": {
        "health": 100,
        "damage": 8,
        "speed": 2.5,
        "color": (100, 100, 200),  # Light blue
        "reward": 30
    },
    "ELITE": {
        "health": 200,
        "damage": 12,
        "speed": 2.2,
        "color": (200, 100, 200),  # Purple
        "reward": 50
    },
    "BOSS": {
        "health": 400,
        "damage": 20,
        "speed": 1.8,
        "color": (255, 50, 50),  # Bright red
        "reward": 100
    }
}

# Enemy spawn weights by round range
# Format: (start_round, {enemy_type: spawn_weight})
ENEMY_SPAWN_WEIGHTS = [
    (1, {  # Rounds 1-2
        "BASIC": 100,
        "STANDARD": 0,
        "ADVANCED": 0,
        "ELITE": 0,
        "BOSS": 0
    }),
    (3, {  # Rounds 3-4
        "BASIC": 70,
        "STANDARD": 30,
        "ADVANCED": 0,
        "ELITE": 0,
        "BOSS": 0
    }),
    (5, {  # Rounds 5-7
        "BASIC": 40,
        "STANDARD": 50,
        "ADVANCED": 10,
        "ELITE": 0,
        "BOSS": 0
    }),
    (8, {  # Rounds 8-9
        "BASIC": 20,
        "STANDARD": 40,
        "ADVANCED": 30,
        "ELITE": 10,
        "BOSS": 0
    }),
    (10, {  # Rounds 10+
        "BASIC": 10,
        "STANDARD": 30,
        "ADVANCED": 40,
        "ELITE": 15,
        "BOSS": 5
    })
]

# Game States
class GameStates:
    MENU = "menu"
    PLAYING = "playing"
    SHOPPING = "shopping"
    ROUND_TRANSITION = "round_transition"
    GAME_OVER = "game_over" 

# UI Colors
ITEM_RARITY_COLORS = {
    "COMMON": (200, 200, 200),    # Light gray
    "RARE": (30, 144, 255),       # Dodger blue
    "EPIC": (147, 112, 219),      # Medium purple
    "LEGENDARY": (255, 140, 0)     # Dark orange
}

# UI Settings
UI_PANEL_COLOR = (40, 44, 52)
UI_ELEMENT_COLOR = (50, 55, 65)
UI_HOVER_COLOR = (60, 65, 75)
UI_SELECTED_COLOR = (70, 75, 85)
UI_BORDER_COLOR = (80, 85, 95)
UI_TEXT_COLOR = (220, 220, 220)
UI_TITLE_SIZE = 48
UI_TEXT_SIZE = 32
UI_SMALL_TEXT_SIZE = 24 