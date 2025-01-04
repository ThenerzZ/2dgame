from enum import Enum
import pygame

class MonsterType(Enum):
    # Basic Enemies (Tier 1)
    SLIME = "slime"
    RAT = "rat"
    BAT = "bat"
    
    # Standard Enemies (Tier 2)
    SKELETON = "skeleton"
    ZOMBIE = "zombie"
    SPIDER = "spider"
    
    # Advanced Enemies (Tier 3)
    DEMON = "demon"
    GOLEM = "golem"
    WITCH = "witch"
    
    # Elite Enemies (Tier 4)
    DRAGON = "dragon"
    NECROMANCER = "necromancer"
    VAMPIRE = "vampire"
    
    # Boss Enemies (Tier 5)
    GHOST = "ghost"
    DEMON_LORD = "demon_lord"
    LICH = "lich"

class DifficultyTier(Enum):
    BASIC = 1
    STANDARD = 2
    ADVANCED = 3
    ELITE = 4
    BOSS = 5

# Helper functions for enemy spawning
def get_enemy_pool_for_round(round_number: int):
    """Get the weighted enemy pool for a specific round"""
    # Get difficulty weights for the round, or use default for high rounds
    if round_number in ROUND_DIFFICULTY:
        weights = ROUND_DIFFICULTY[round_number]
    else:
        weights = DEFAULT_HIGH_ROUND_WEIGHTS
    
    # Build pool of eligible enemies with their weights
    enemy_pool = []
    for monster_type in MonsterType:
        monster_tier = MONSTER_TIERS[monster_type]
        if monster_tier in weights:
            enemy_pool.append({
                'type': monster_type,
                'weight': weights[monster_tier]
            })
    
    return enemy_pool

def get_monster_stats(monster_type: MonsterType, round_number: int = 1):
    """Get monster stats with scaling based on round number"""
    base_stats = MONSTER_CONFIG[monster_type]["base_stats"].copy()
    
    # Scale stats based on round number (10% increase per round after base round)
    base_round = MONSTER_TIERS[monster_type].value * 2  # Higher tier enemies scale from later rounds
    if round_number > base_round:
        scaling = 1 + (round_number - base_round) * 0.1
        base_stats["health"] = int(base_stats["health"] * scaling)
        base_stats["damage"] = int(base_stats["damage"] * scaling)
        base_stats["exp_reward"] = int(base_stats["exp_reward"] * (1 + (round_number - base_round) * 0.05))
    
    return base_stats

# Mapping of rounds to difficulty weights
ROUND_DIFFICULTY = {
    # Round: {Tier: Spawn Weight}
    1: {DifficultyTier.BASIC: 100},
    2: {DifficultyTier.BASIC: 80, DifficultyTier.STANDARD: 20},
    3: {DifficultyTier.BASIC: 60, DifficultyTier.STANDARD: 40},
    4: {DifficultyTier.BASIC: 40, DifficultyTier.STANDARD: 50, DifficultyTier.ADVANCED: 10},
    5: {DifficultyTier.BASIC: 30, DifficultyTier.STANDARD: 50, DifficultyTier.ADVANCED: 20},
    6: {DifficultyTier.BASIC: 20, DifficultyTier.STANDARD: 40, DifficultyTier.ADVANCED: 35, DifficultyTier.ELITE: 5},
    7: {DifficultyTier.STANDARD: 30, DifficultyTier.ADVANCED: 50, DifficultyTier.ELITE: 20},
    8: {DifficultyTier.STANDARD: 20, DifficultyTier.ADVANCED: 50, DifficultyTier.ELITE: 30},
    9: {DifficultyTier.ADVANCED: 40, DifficultyTier.ELITE: 50, DifficultyTier.BOSS: 10},
    10: {DifficultyTier.ADVANCED: 20, DifficultyTier.ELITE: 60, DifficultyTier.BOSS: 20}
}

# Default weights for higher rounds
DEFAULT_HIGH_ROUND_WEIGHTS = {
    DifficultyTier.ADVANCED: 30,
    DifficultyTier.ELITE: 50,
    DifficultyTier.BOSS: 20
}

# Mapping of monster types to their difficulty tiers
MONSTER_TIERS = {
    # Basic Enemies
    MonsterType.SLIME: DifficultyTier.BASIC,
    MonsterType.RAT: DifficultyTier.BASIC,
    MonsterType.BAT: DifficultyTier.BASIC,
    
    # Standard Enemies
    MonsterType.SKELETON: DifficultyTier.STANDARD,
    MonsterType.ZOMBIE: DifficultyTier.STANDARD,
    MonsterType.SPIDER: DifficultyTier.STANDARD,
    
    # Advanced Enemies
    MonsterType.DEMON: DifficultyTier.ADVANCED,
    MonsterType.GOLEM: DifficultyTier.ADVANCED,
    MonsterType.WITCH: DifficultyTier.ADVANCED,
    
    # Elite Enemies
    MonsterType.DRAGON: DifficultyTier.ELITE,
    MonsterType.NECROMANCER: DifficultyTier.ELITE,
    MonsterType.VAMPIRE: DifficultyTier.ELITE,
    
    # Boss Enemies
    MonsterType.GHOST: DifficultyTier.BOSS,
    MonsterType.DEMON_LORD: DifficultyTier.BOSS,
    MonsterType.LICH: DifficultyTier.BOSS
}

# Monster configuration with all properties in one place
MONSTER_CONFIG = {
    # BASIC TIER ENEMIES
    MonsterType.SLIME: {
        "tier": "BASIC",
        "base_stats": {
            "health": 40,
            "damage": 3,
            "speed": 2,
            "exp_reward": 1,
        },
        "colors": {
            "primary": [(100, 200, 50, 160), (50, 150, 200, 160), (150, 50, 200, 160)],
        },
        "sprite_config": {
            "parts": ["body"],
            "size_ratio": {"body": 2/3}
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["splat", "fade"],
            "particle_config": {
                "type": "splash",
                "count": 8,
                "speed": (1, 3),
                "size": (2, 4),
                "lifetime": (20, 40)
            }
        }
    },
    
    MonsterType.RAT: {
        "tier": "BASIC",
        "base_stats": {
            "health": 30,
            "damage": 4,
            "speed": 3,
            "exp_reward": 1,
        },
        "colors": {
            "primary": [(100, 90, 80), (80, 70, 60)],
            "secondary": [(200, 50, 50)]  # Red eyes
        },
        "sprite_config": {
            "parts": ["body", "tail", "ears"],
            "size_ratio": {
                "body": 1/2,
                "tail": 1/4,
                "ears": 1/6
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["fade"],
            "particle_config": {
                "type": "dust",
                "count": 5,
                "speed": (1, 2),
                "size": (2, 3),
                "lifetime": (20, 30)
            }
        }
    },
    
    MonsterType.BAT: {
        "tier": "BASIC",
        "base_stats": {
            "health": 25,
            "damage": 3,
            "speed": 4,
            "exp_reward": 1,
        },
        "colors": {
            "primary": [(40, 40, 40), (60, 60, 60)],
            "secondary": [(150, 0, 0)]  # Red eyes
        },
        "sprite_config": {
            "parts": ["body", "wings"],
            "size_ratio": {
                "body": 1/3,
                "wings": 2/3
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["scatter", "fade"],
            "particle_config": {
                "type": "feather",
                "count": 6,
                "speed": (1, 2),
                "size": (2, 3),
                "lifetime": (30, 40)
            }
        }
    },
    
    # STANDARD TIER ENEMIES
    MonsterType.SKELETON: {
        "tier": "STANDARD",
        "base_stats": {
            "health": 60,
            "damage": 5,
            "speed": 3,
            "exp_reward": 2,
        },
        "colors": {
            "primary": [(200, 190, 180), (180, 170, 160), (160, 150, 140)],
            "secondary": [(255, 50, 50), (255, 200, 50), (50, 255, 50)],
        },
        "sprite_config": {
            "parts": ["skull", "ribcage", "arms"],
            "size_ratio": {
                "skull": 1/3,
                "ribcage": 1/2,
                "arms": 1/3,
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["scatter", "fade"],
            "particle_config": {
                "type": "bone",
                "count": 6,
                "speed": (2, 4),
                "size": (3, 5),
                "lifetime": (30, 50),
                "physics": {"gravity": 0.2, "rotation": True}
            }
        }
    },
    
    MonsterType.ZOMBIE: {
        "tier": "STANDARD",
        "base_stats": {
            "health": 80,
            "damage": 6,
            "speed": 2,
            "exp_reward": 2,
        },
        "colors": {
            "primary": [(50, 100, 50), (70, 90, 70)],
            "secondary": [(30, 60, 30)]
        },
        "sprite_config": {
            "parts": ["body", "arms", "head"],
            "size_ratio": {
                "body": 2/3,
                "arms": 1/4,
                "head": 1/3
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["dissolve", "fade"],
            "particle_config": {
                "type": "gore",
                "count": 8,
                "speed": (1, 2),
                "size": (3, 4),
                "lifetime": (30, 40)
            }
        }
    },
    
    MonsterType.SPIDER: {
        "tier": "STANDARD",
        "base_stats": {
            "health": 50,
            "damage": 8,
            "speed": 3.5,
            "exp_reward": 2,
        },
        "colors": {
            "primary": [(40, 35, 30), (60, 50, 40), (30, 25, 20)],
        },
        "sprite_config": {
            "parts": ["body", "legs"],
            "size_ratio": {
                "body": 1/2,
                "legs": 1/4,
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["curl", "fade"],
            "particle_config": {
                "type": "web",
                "count": 12,
                "speed": (1, 2),
                "size": (1, 3),
                "lifetime": (40, 60)
            }
        }
    },
    
    # ADVANCED TIER ENEMIES
    MonsterType.DEMON: {
        "tier": "ADVANCED",
        "base_stats": {
            "health": 120,
            "damage": 12,
            "speed": 2.8,
            "exp_reward": 3,
        },
        "colors": {
            "primary": [(140, 50, 50), (150, 100, 100)],
            "secondary": [(255, 100, 0), (200, 50, 0)],
        },
        "sprite_config": {
            "parts": ["body", "horns", "wings"],
            "size_ratio": {
                "body": 2/3,
                "horns": 1/4,
                "wings": 1/2,
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["burn", "fade"],
            "particle_config": {
                "type": "fire",
                "count": 15,
                "speed": (1, 3),
                "size": (3, 6),
                "lifetime": (30, 50),
                "colors": [(255, 100, 0), (200, 50, 0), (150, 150, 150)]
            }
        }
    },
    
    MonsterType.GOLEM: {
        "tier": "ADVANCED",
        "base_stats": {
            "health": 200,
            "damage": 15,
            "speed": 1.5,
            "exp_reward": 3,
        },
        "colors": {
            "primary": [(100, 100, 100), (80, 80, 80)],
            "secondary": [(150, 150, 0)]  # Glowing runes
        },
        "sprite_config": {
            "parts": ["body", "arms", "core"],
            "size_ratio": {
                "body": 3/4,
                "arms": 1/3,
                "core": 1/4
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["crumble", "fade"],
            "particle_config": {
                "type": "rock",
                "count": 12,
                "speed": (2, 4),
                "size": (4, 6),
                "lifetime": (40, 60),
                "physics": {"gravity": 0.3}
            }
        }
    },
    
    MonsterType.WITCH: {
        "tier": "ADVANCED",
        "base_stats": {
            "health": 90,
            "damage": 18,
            "speed": 2.5,
            "exp_reward": 3,
        },
        "colors": {
            "primary": [(100, 0, 100), (80, 0, 80)],
            "secondary": [(200, 50, 200)]
        },
        "sprite_config": {
            "parts": ["body", "hat", "staff"],
            "size_ratio": {
                "body": 2/3,
                "hat": 1/3,
                "staff": 1/2
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["magic_burst", "fade"],
            "particle_config": {
                "type": "magic",
                "count": 15,
                "speed": (2, 4),
                "size": (3, 5),
                "lifetime": (40, 60),
                "colors": [(200, 50, 200), (150, 0, 150), (100, 0, 100)]
            }
        }
    },
    
    # ELITE TIER ENEMIES
    MonsterType.DRAGON: {
        "tier": "ELITE",
        "base_stats": {
            "health": 300,
            "damage": 25,
            "speed": 2.2,
            "exp_reward": 5,
        },
        "colors": {
            "primary": [(150, 0, 0), (120, 0, 0)],
            "secondary": [(255, 150, 0)]
        },
        "sprite_config": {
            "parts": ["body", "wings", "head"],
            "size_ratio": {
                "body": 3/4,
                "wings": 1,
                "head": 1/3
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["explosion", "fade"],
            "particle_config": {
                "type": "flame",
                "count": 20,
                "speed": (3, 5),
                "size": (4, 8),
                "lifetime": (50, 70),
                "colors": [(255, 150, 0), (255, 100, 0), (200, 50, 0)]
            }
        }
    },
    
    MonsterType.NECROMANCER: {
        "tier": "ELITE",
        "base_stats": {
            "health": 250,
            "damage": 30,
            "speed": 2,
            "exp_reward": 5,
        },
        "colors": {
            "primary": [(50, 0, 50), (30, 0, 30)],
            "secondary": [(0, 255, 0)]
        },
        "sprite_config": {
            "parts": ["body", "cloak", "staff"],
            "size_ratio": {
                "body": 2/3,
                "cloak": 1,
                "staff": 3/4
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["soul_release", "fade"],
            "particle_config": {
                "type": "soul",
                "count": 18,
                "speed": (2, 4),
                "size": (4, 6),
                "lifetime": (45, 65),
                "colors": [(0, 255, 0), (0, 200, 0), (0, 150, 0)]
            }
        }
    },
    
    MonsterType.VAMPIRE: {
        "tier": "ELITE",
        "base_stats": {
            "health": 280,
            "damage": 28,
            "speed": 2.5,
            "exp_reward": 5,
        },
        "colors": {
            "primary": [(80, 0, 0), (60, 0, 0)],
            "secondary": [(200, 0, 0)]
        },
        "sprite_config": {
            "parts": ["body", "cape", "head"],
            "size_ratio": {
                "body": 2/3,
                "cape": 1,
                "head": 1/3
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["blood_mist", "fade"],
            "particle_config": {
                "type": "blood",
                "count": 16,
                "speed": (2, 4),
                "size": (3, 5),
                "lifetime": (40, 60),
                "colors": [(200, 0, 0), (150, 0, 0), (100, 0, 0)]
            }
        }
    },
    
    # BOSS TIER ENEMIES
    MonsterType.GHOST: {
        "tier": "BOSS",
        "base_stats": {
            "health": 400,
            "damage": 20,
            "speed": 1.8,
            "exp_reward": 8,
        },
        "colors": {
            "primary": [(200, 200, 255, 160), (180, 180, 255, 160)],
        },
        "sprite_config": {
            "parts": ["body", "aura"],
            "size_ratio": {
                "body": 3/4,
                "aura": 1,
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["dissipate", "fade"],
            "particle_config": {
                "type": "ethereal",
                "count": 20,
                "speed": (0.5, 1.5),
                "size": (2, 5),
                "lifetime": (50, 70),
                "pulse": True
            }
        }
    },
    
    MonsterType.DEMON_LORD: {
        "tier": "BOSS",
        "base_stats": {
            "health": 500,
            "damage": 35,
            "speed": 2,
            "exp_reward": 10,
        },
        "colors": {
            "primary": [(200, 0, 0), (150, 0, 0)],
            "secondary": [(255, 150, 0), (255, 100, 0)]
        },
        "sprite_config": {
            "parts": ["body", "wings", "horns", "crown"],
            "size_ratio": {
                "body": 3/4,
                "wings": 1,
                "horns": 1/3,
                "crown": 1/4
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["hellfire", "fade"],
            "particle_config": {
                "type": "hellfire",
                "count": 25,
                "speed": (3, 6),
                "size": (5, 10),
                "lifetime": (60, 80),
                "colors": [(255, 100, 0), (255, 50, 0), (200, 0, 0)]
            }
        }
    },
    
    MonsterType.LICH: {
        "tier": "BOSS",
        "base_stats": {
            "health": 450,
            "damage": 40,
            "speed": 1.5,
            "exp_reward": 10,
        },
        "colors": {
            "primary": [(50, 50, 80), (30, 30, 60)],
            "secondary": [(0, 255, 255)]
        },
        "sprite_config": {
            "parts": ["body", "robe", "crown", "staff"],
            "size_ratio": {
                "body": 2/3,
                "robe": 1,
                "crown": 1/4,
                "staff": 3/4
            }
        },
        "death_animation": {
            "frame_count": 3,
            "frame_duration": 15,
            "effects": ["phylactery", "fade"],
            "particle_config": {
                "type": "arcane",
                "count": 30,
                "speed": (2, 5),
                "size": (4, 8),
                "lifetime": (55, 75),
                "colors": [(0, 255, 255), (0, 200, 200), (0, 150, 150)]
            }
        }
    }
}

# Helper functions for accessing monster configuration
def get_monster_config(monster_type: MonsterType):
    """Get the configuration for a specific monster type"""
    return MONSTER_CONFIG[monster_type]

def get_monster_tier(monster_type: MonsterType):
    """Get the tier of a specific monster type"""
    return MONSTER_CONFIG[monster_type]["tier"]

def get_monster_colors(monster_type: MonsterType):
    """Get the color palette for a specific monster type"""
    return MONSTER_CONFIG[monster_type]["colors"]

def get_death_config(monster_type: MonsterType):
    """Get the death animation configuration for a specific monster type"""
    return MONSTER_CONFIG[monster_type]["death_animation"] 