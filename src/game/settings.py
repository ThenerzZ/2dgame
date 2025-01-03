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
STARTING_ENEMIES = 5
ENEMY_SPAWN_RATE = 1.0
ENEMY_KILL_REWARD = 15
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