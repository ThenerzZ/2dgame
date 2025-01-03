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
        pass
        
    def remove_effect(self, player):
        """Remove the item's effect from the player"""
        pass
        
    def on_purchase(self, player):
        """Called when the item is purchased"""
        pass
        
    def get_display_color(self):
        """Get the color for displaying the item based on rarity"""
        colors = {
            ItemRarity.COMMON: (200, 200, 200),    # Gray
            ItemRarity.RARE: (0, 112, 221),        # Blue
            ItemRarity.EPIC: (163, 53, 238),       # Purple
            ItemRarity.LEGENDARY: (255, 128, 0),   # Orange
        }
        return colors.get(self.rarity) 