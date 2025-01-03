from items.item_base import Item, ItemRarity, ItemType

# Weapon Items (Active)
class MagicWand(Item):
    def __init__(self):
        super().__init__(
            name="Magic Wand",
            description="Shoots a magical projectile that bounces between enemies",
            rarity=ItemRarity.COMMON,
            item_type=ItemType.ACTIVE,
            cost=50,
            stats={
                "damage": 15,
                "projectile_speed": 8,
                "bounce_count": 2,
                "cooldown": 1.5  # seconds
            }
        )

class Knife(Item):
    def __init__(self):
        super().__init__(
            name="Knife",
            description="Throws knives in the direction you're facing",
            rarity=ItemRarity.COMMON,
            item_type=ItemType.ACTIVE,
            cost=50,
            stats={
                "damage": 10,
                "projectile_speed": 12,
                "penetration": 1,
                "cooldown": 1.0
            }
        )

class Whip(Item):
    def __init__(self):
        super().__init__(
            name="Whip",
            description="Attacks enemies in a wide arc in front of you",
            rarity=ItemRarity.COMMON,
            item_type=ItemType.ACTIVE,
            cost=50,
            stats={
                "damage": 20,
                "arc_degrees": 120,
                "range": 100,
                "cooldown": 1.2
            }
        )

class FireWand(Item):
    def __init__(self):
        super().__init__(
            name="Fire Wand",
            description="Shoots fireballs that explode on impact",
            rarity=ItemRarity.RARE,
            item_type=ItemType.ACTIVE,
            cost=75,
            stats={
                "damage": 25,
                "explosion_radius": 50,
                "burn_damage": 5,
                "burn_duration": 3,
                "cooldown": 2.0
            }
        )

class CrossBow(Item):
    def __init__(self):
        super().__init__(
            name="Cross Bow",
            description="Fires multiple arrows in a spread pattern",
            rarity=ItemRarity.RARE,
            item_type=ItemType.ACTIVE,
            cost=75,
            stats={
                "damage": 15,
                "arrow_count": 3,
                "spread_angle": 30,
                "cooldown": 1.8
            }
        )

class LightningRing(Item):
    def __init__(self):
        super().__init__(
            name="Lightning Ring",
            description="Creates chain lightning between nearby enemies",
            rarity=ItemRarity.EPIC,
            item_type=ItemType.ACTIVE,
            cost=100,
            stats={
                "damage": 30,
                "chain_count": 3,
                "chain_range": 120,
                "cooldown": 2.5
            }
        )

# Passive Items
class Wings(Item):
    def __init__(self):
        super().__init__(
            name="Wings",
            description="Increases movement speed and allows passing through enemies",
            rarity=ItemRarity.RARE,
            item_type=ItemType.PASSIVE,
            cost=75,
            stats={
                "move_speed": 1.3,
                "phase_through": True
            }
        )

class Spinach(Item):
    def __init__(self):
        super().__init__(
            name="Spinach",
            description="Increases all damage by 20%",
            rarity=ItemRarity.COMMON,
            item_type=ItemType.PASSIVE,
            cost=50,
            stats={"damage_multiplier": 1.2}
        )

class EmptyTome(Item):
    def __init__(self):
        super().__init__(
            name="Empty Tome",
            description="Reduces weapon cooldown by 15%",
            rarity=ItemRarity.COMMON,
            item_type=ItemType.PASSIVE,
            cost=50,
            stats={"cooldown_reduction": 0.85}
        )

class Clover(Item):
    def __init__(self):
        super().__init__(
            name="Clover",
            description="Increases luck and critical hit chance",
            rarity=ItemRarity.RARE,
            item_type=ItemType.PASSIVE,
            cost=75,
            stats={
                "crit_chance": 0.1,
                "luck": 1.2
            }
        )

class Crown(Item):
    def __init__(self):
        super().__init__(
            name="Crown",
            description="Increases experience gain by 30%",
            rarity=ItemRarity.RARE,
            item_type=ItemType.PASSIVE,
            cost=75,
            stats={"exp_multiplier": 1.3}
        )

class HollowHeart(Item):
    def __init__(self):
        super().__init__(
            name="Hollow Heart",
            description="Increases max HP and recovery effects",
            rarity=ItemRarity.RARE,
            item_type=ItemType.PASSIVE,
            cost=75,
            stats={
                "max_health_multiplier": 1.25,
                "healing_multiplier": 1.2
            }
        )

class Bracer(Item):
    def __init__(self):
        super().__init__(
            name="Bracer",
            description="Increases projectile speed and size",
            rarity=ItemRarity.COMMON,
            item_type=ItemType.PASSIVE,
            cost=50,
            stats={
                "projectile_speed": 1.2,
                "projectile_size": 1.1
            }
        )

class Magnet(Item):
    def __init__(self):
        super().__init__(
            name="Magnet",
            description="Increases pickup radius for items and experience",
            rarity=ItemRarity.COMMON,
            item_type=ItemType.PASSIVE,
            cost=50,
            stats={"pickup_radius": 1.5}
        )

# Evolution combinations (to be implemented)
EVOLUTION_PAIRS = {
    ("Magic Wand", "Empty Tome"): "Holy Wand",
    ("Knife", "Bracer"): "Thousand Edge",
    ("Whip", "Hollow Heart"): "Bloody Tear",
    ("Fire Wand", "Spinach"): "Hellfire",
    ("CrossBow", "Clover"): "Phieraggi",
    ("Lightning Ring", "Crown"): "Thunder Loop"
}

# List of all available items
ITEM_POOL = [
    MagicWand(),
    Knife(),
    Whip(),
    FireWand(),
    CrossBow(),
    LightningRing(),
    Wings(),
    Spinach(),
    EmptyTome(),
    Clover(),
    Crown(),
    HollowHeart(),
    Bracer(),
    Magnet()
] 