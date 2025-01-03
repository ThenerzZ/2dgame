class Inventory:
    def __init__(self, max_size=20):
        self.items = []
        self.max_size = max_size
        self.active_items = []  # Items currently affecting the player
        self.player = None  # Will be set when added to player
        
    def set_player(self, player):
        """Set the player reference"""
        self.player = player
        
    def add_item(self, item):
        """Add an item to the inventory"""
        if len(self.items) < self.max_size:
            self.items.append(item)
            if item.item_type.PASSIVE and self.player:
                self.active_items.append(item)
                item.apply_effect(self.player)
            return True
        return False
        
    def remove_item(self, item):
        """Remove an item from the inventory"""
        if item in self.items:
            self.items.remove(item)
            if item in self.active_items and self.player:
                self.active_items.remove(item)
                item.remove_effect(self.player)
            return True
        return False
        
    def get_items_by_type(self, item_type):
        """Get all items of a specific type"""
        return [item for item in self.items if item.item_type == item_type]
        
    def get_active_effects(self):
        """Get all currently active effects"""
        return [item.stats for item in self.active_items]
        
    def clear(self):
        """Clear the inventory"""
        if self.player:
            for item in self.active_items:
                item.remove_effect(self.player)
        self.items.clear()
        self.active_items.clear() 