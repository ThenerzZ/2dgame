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

# UI Colors for Dark Fantasy Theme
UI_COLORS = {
    "BACKGROUND": (15, 12, 16),       # Very dark purple-black
    "PANEL": (28, 21, 32),            # Dark purple-gray
    "PANEL_LIGHT": (38, 28, 42),      # Lighter purple-gray
    "BORDER": (66, 40, 90),           # Deep purple
    "BORDER_HIGHLIGHT": (94, 53, 177), # Bright purple
    "TEXT": (220, 215, 225),          # Off-white
    "TEXT_DARK": (150, 142, 155),     # Darker text
    "ACCENT": (163, 92, 255),         # Bright purple accent
    "ACCENT_DARK": (102, 51, 153),    # Darker purple accent
    "HEALTH": (178, 34, 34),          # Blood red
    "MANA": (51, 153, 255),           # Bright blue
    "GOLD": (255, 215, 0),            # Gold
    "SUCCESS": (0, 255, 128),         # Emerald green
    "WARNING": (255, 140, 0),         # Orange
    "DANGER": (220, 20, 60)           # Crimson
}

# Item Rarity Colors (Dark Fantasy Theme)
ITEM_RARITY_COLORS = {
    "COMMON": (180, 180, 190),        # Steel gray
    "UNCOMMON": (0, 255, 128),        # Emerald green
    "RARE": (51, 153, 255),           # Sapphire blue
    "EPIC": (163, 92, 255),           # Royal purple
    "LEGENDARY": (255, 140, 0),       # Burning orange
    "MYTHIC": (255, 0, 127)           # Deep pink
}

# UI Settings
UI_FONT_FAMILY = "medieval"  # Will be loaded from assets
UI_TITLE_SIZE = 48
UI_HEADING_SIZE = 36
UI_TEXT_SIZE = 24
UI_SMALL_TEXT_SIZE = 18

# UI Element Sizes
UI_BUTTON_HEIGHT = 50
UI_BUTTON_WIDTH = 200
UI_PANEL_PADDING = 20
UI_BORDER_WIDTH = 2
UI_ICON_SIZE = 32

# Animation Timings
UI_FADE_DURATION = 0.3
UI_SLIDE_DURATION = 0.4
TOOLTIP_DELAY = 0.5

# Menu Settings
MENU_OPTIONS = {
    "MAIN": [
        "Continue",
        "New Game",
        "Settings",
        "Credits",
        "Exit"
    ],
    "SETTINGS": [
        "Graphics",
        "Sound",
        "Controls",
        "Gameplay",
        "Back"
    ],
    "GRAPHICS": [
        "Resolution",
        "Fullscreen",
        "VSync",
        "Effects Quality",
        "Back"
    ],
    "SOUND": [
        "Master Volume",
        "Music Volume",
        "Effects Volume",
        "Back"
    ],
    "CONTROLS": [
        "Key Bindings",
        "Mouse Sensitivity",
        "Controller",
        "Back"
    ],
    "GAMEPLAY": [
        "Difficulty",
        "Tutorial Tips",
        "Combat Numbers",
        "Screen Shake",
        "Back"
    ]
} 