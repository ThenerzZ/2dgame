from enum import Enum

class ItemRarity(Enum):
    COMMON = 1
    RARE = 2
    EPIC = 3
    LEGENDARY = 4

class ItemType(Enum):
    PASSIVE = 1    # Items that give passive bonuses
    ACTIVE = 2     # Items with active abilities
    CONSUMABLE = 3 # One-time use items

class Item:
    def __init__(self, name, description, rarity, item_type, cost, stats=None):
        self.name = name
        self.description = description
        self.rarity = rarity
        self.item_type = item_type
        self.cost = cost
        self.stats = stats or {}
        
    def apply_effect(self, player):
        """Apply the item's effect to the player"""
        # Apply stats
        for stat_name, value in self.stats.items():
            if isinstance(value, (int, float)):
                if stat_name in player.stats:
                    player.stats[stat_name] += value
                else:
                    player.stats[stat_name] = value
            elif isinstance(value, dict):
                # For more complex stats like cooldown_reduction
                for sub_stat, sub_value in value.items():
                    player.stats[f"{stat_name}_{sub_stat}"] = sub_value
        
    def remove_effect(self, player):
        """Remove the item's effect from the player"""
        # Remove stats
        for stat_name, value in self.stats.items():
            if isinstance(value, (int, float)):
                if stat_name in player.stats:
                    player.stats[stat_name] -= value
            elif isinstance(value, dict):
                for sub_stat in value.keys():
                    player.stats.pop(f"{stat_name}_{sub_stat}", None)
        
    def on_purchase(self, player):
        """Called when the item is purchased"""
        self.apply_effect(player)
        
    def get_display_color(self):
        """Get the color for displaying the item based on rarity"""
        colors = {
            ItemRarity.COMMON: (200, 200, 200),    # Gray
            ItemRarity.RARE: (0, 112, 221),        # Blue
            ItemRarity.EPIC: (163, 53, 238),       # Purple
            ItemRarity.LEGENDARY: (255, 128, 0),   # Orange
        }
        return colors.get(self.rarity)

# Base classes for different item types
class WeaponItem(Item):
    def __init__(self, name, description, rarity, cost, stats=None, weapon_stats=None):
        super().__init__(name, description, rarity, ItemType.ACTIVE, cost, stats)
        self.weapon_stats = weapon_stats or {}
        
    def apply_effect(self, player):
        super().apply_effect(player)
        # Apply weapon-specific stats
        for stat, value in self.weapon_stats.items():
            player.stats[f"weapon_{stat}"] = value

    def remove_effect(self, player):
        super().remove_effect(player)
        # Remove weapon-specific stats
        for stat in self.weapon_stats.keys():
            player.stats.pop(f"weapon_{stat}", None)

class PassiveItem(Item):
    def __init__(self, name, description, rarity, cost, stats=None, passive_effect=None):
        super().__init__(name, description, rarity, ItemType.PASSIVE, cost, stats)
        self.passive_effect = passive_effect
        
    def apply_effect(self, player):
        super().apply_effect(player)
        if self.passive_effect:
            self.passive_effect(player)

class ConsumableItem(Item):
    def __init__(self, name, description, rarity, cost, use_effect=None):
        super().__init__(name, description, rarity, ItemType.CONSUMABLE, cost)
        self.use_effect = use_effect
        
    def use(self, player):
        """Use the consumable item"""
        if self.use_effect:
            self.use_effect(player)
            return True
        return False 