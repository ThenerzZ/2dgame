from items.item_base import Item, ItemRarity, ItemType

class HealthBoost(Item):
    def __init__(self):
        super().__init__(
            name="Health Boost",
            description="Increases max health by 20%",
            rarity=ItemRarity.COMMON,
            item_type=ItemType.PASSIVE,
            cost=50,
            stats={"max_health": 1.2}
        )
    
    def apply_effect(self, player):
        player.max_health *= self.stats["max_health"]
        player.health = player.max_health

class SpeedBoots(Item):
    def __init__(self):
        super().__init__(
            name="Speed Boots",
            description="Increases movement speed by 15%",
            rarity=ItemRarity.COMMON,
            item_type=ItemType.PASSIVE,
            cost=50,
            stats={"move_speed": 1.15}
        )
    
    def apply_effect(self, player):
        player.modify_stat("move_speed", self.stats["move_speed"])
    
    def remove_effect(self, player):
        player.modify_stat("move_speed", 1 / self.stats["move_speed"])

class PowerGloves(Item):
    def __init__(self):
        super().__init__(
            name="Power Gloves",
            description="Increases damage by 25%",
            rarity=ItemRarity.RARE,
            item_type=ItemType.PASSIVE,
            cost=75,
            stats={"damage": 1.25}
        )
    
    def apply_effect(self, player):
        player.modify_stat("damage", self.stats["damage"])
    
    def remove_effect(self, player):
        player.modify_stat("damage", 1 / self.stats["damage"])

class Shield(Item):
    def __init__(self):
        super().__init__(
            name="Shield",
            description="Increases defense by 10",
            rarity=ItemRarity.RARE,
            item_type=ItemType.PASSIVE,
            cost=75,
            stats={"defense": 10}
        )
    
    def apply_effect(self, player):
        player.stats["defense"] += self.stats["defense"]
    
    def remove_effect(self, player):
        player.stats["defense"] -= self.stats["defense"]

class CriticalStrike(Item):
    def __init__(self):
        super().__init__(
            name="Critical Strike",
            description="Increases critical chance by 10%",
            rarity=ItemRarity.EPIC,
            item_type=ItemType.PASSIVE,
            cost=100,
            stats={"crit_chance": 0.10}
        )
    
    def apply_effect(self, player):
        player.stats["crit_chance"] += self.stats["crit_chance"]
    
    def remove_effect(self, player):
        player.stats["crit_chance"] -= self.stats["crit_chance"]

class LegendaryWeapon(Item):
    def __init__(self):
        super().__init__(
            name="Legendary Weapon",
            description="Increases all damage by 50%",
            rarity=ItemRarity.LEGENDARY,
            item_type=ItemType.PASSIVE,
            cost=150,
            stats={"damage": 1.5, "crit_damage": 1.2}
        )
    
    def apply_effect(self, player):
        player.modify_stat("damage", self.stats["damage"])
        player.modify_stat("crit_damage", self.stats["crit_damage"])
    
    def remove_effect(self, player):
        player.modify_stat("damage", 1 / self.stats["damage"])
        player.modify_stat("crit_damage", 1 / self.stats["crit_damage"])

# List of all available items
ITEM_POOL = [
    HealthBoost(),
    SpeedBoots(),
    PowerGloves(),
    Shield(),
    CriticalStrike(),
    LegendaryWeapon()
] 