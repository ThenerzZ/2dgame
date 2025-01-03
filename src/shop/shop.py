import random
from game.settings import *
from items.item_base import ItemRarity

class Shop:
    def __init__(self):
        self.available_items = []
        self.refresh_cost = SHOP_REFRESH_COST
        self.max_items = SHOP_ITEMS_DISPLAYED
        self.timer = 0
        
    def generate_items(self, item_pool):
        """Generate a new set of items for the shop"""
        self.available_items.clear()
        for _ in range(self.max_items):
            rarity = self._get_random_rarity()
            possible_items = [item for item in item_pool if item.rarity == rarity]
            if possible_items:
                self.available_items.append(random.choice(possible_items))
                
    def _get_random_rarity(self):
        """Get a random rarity based on the configured chances"""
        roll = random.randint(1, 100)
        cumulative = 0
        for rarity, chance in ITEM_RARITY.items():
            cumulative += chance
            if roll <= cumulative:
                return ItemRarity[rarity]
        return ItemRarity.COMMON
        
    def purchase_item(self, player, item_index):
        """Attempt to purchase an item"""
        if 0 <= item_index < len(self.available_items):
            item = self.available_items[item_index]
            if player.money >= item.cost:
                player.money -= item.cost
                player.inventory.add_item(item)
                self.available_items.pop(item_index)
                item.on_purchase(player)
                return True
        return False
        
    def refresh_shop(self, player, item_pool):
        """Refresh the shop's items"""
        if player.money >= self.refresh_cost:
            player.money -= self.refresh_cost
            self.generate_items(item_pool)
            return True
        return False
        
    def update(self, dt):
        """Update shop timer"""
        self.timer += dt
        if self.timer >= SHOP_APPEAR_INTERVAL:
            self.timer = 0
            return True
        return False 