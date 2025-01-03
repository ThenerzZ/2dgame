import pygame
import random
from game.settings import *

class ShopItem:
    def __init__(self, name, cost, rarity, effect):
        self.name = name
        self.cost = cost
        self.rarity = rarity
        self.effect = effect
        self.description = self._generate_description()
        
    def _generate_description(self):
        """Generate item description based on effect"""
        stat, value = self.effect
        if stat == "damage":
            return f"Increases damage by {int(value * 100)}%"
        elif stat == "attack_speed":
            return f"Increases attack speed by {int(value * 100)}%"
        elif stat == "move_speed":
            return f"Increases movement speed by {int(value * 100)}%"
        elif stat == "max_health":
            return f"Increases max health by {int(value * 100)}%"
        elif stat == "defense":
            return f"Increases defense by {int(value * 100)}%"
        elif stat == "crit_chance":
            return f"Increases critical chance by {int(value * 100)}%"
        return "Unknown effect"

class Shop:
    def __init__(self):
        self.items = []
        self.selected_item = None
        self.refresh_cost = SHOP_REFRESH_COST
        
        # Define possible items and their base stats
        self.possible_items = {
            "Sword": ("damage", 0.15),
            "Boots": ("move_speed", 0.1),
            "Shield": ("defense", 0.1),
            "Heart": ("max_health", 0.15),
            "Gloves": ("attack_speed", 0.1),
            "Crystal": ("crit_chance", 0.05),
        }
        
        # Initial refresh
        self.refresh_items()
        
    def refresh_items(self):
        """Refresh shop items"""
        self.items.clear()
        
        # Generate new items
        for _ in range(SHOP_ITEMS_DISPLAYED):
            # Select rarity based on chances
            rarity = self._select_rarity()
            
            # Select random item type
            item_name = random.choice(list(self.possible_items.keys()))
            stat, base_value = self.possible_items[item_name]
            
            # Scale value and cost based on rarity
            value_multiplier = {
                "COMMON": 1.0,
                "RARE": 1.5,
                "EPIC": 2.0,
                "LEGENDARY": 3.0
            }[rarity]
            
            value = base_value * value_multiplier
            cost = int(50 * value_multiplier)
            
            # Create item
            item = ShopItem(
                name=f"{rarity} {item_name}",
                cost=cost,
                rarity=rarity,
                effect=(stat, value)
            )
            self.items.append(item)
            
    def _select_rarity(self):
        """Select item rarity based on chances"""
        roll = random.randint(1, 100)
        if roll <= ITEM_RARITY["COMMON"]:
            return "COMMON"
        elif roll <= ITEM_RARITY["COMMON"] + ITEM_RARITY["RARE"]:
            return "RARE"
        elif roll <= ITEM_RARITY["COMMON"] + ITEM_RARITY["RARE"] + ITEM_RARITY["EPIC"]:
            return "EPIC"
        else:
            return "LEGENDARY"
            
    def update(self):
        """Update shop state"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        # Handle item selection and purchase
        if mouse_clicked:
            self._handle_click(mouse_pos)
            
    def _handle_click(self, pos):
        """Handle mouse click in shop"""
        # Check item clicks
        for i, item in enumerate(self.items):
            item_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - 200,
                100 + i * 100,
                400,
                80
            )
            if item_rect.collidepoint(pos):
                self.selected_item = item
                break
                
        # Check refresh button
        refresh_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT - 100,
            200,
            50
        )
        if refresh_rect.collidepoint(pos):
            self.refresh_items()
            
    def draw(self, screen):
        """Draw shop interface"""
        # Draw background
        pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Draw items
        for i, item in enumerate(self.items):
            # Item background
            item_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - 200,
                100 + i * 100,
                400,
                80
            )
            color = {
                "COMMON": (200, 200, 200),
                "RARE": (100, 100, 255),
                "EPIC": (200, 100, 255),
                "LEGENDARY": (255, 215, 0)
            }[item.rarity]
            pygame.draw.rect(screen, color, item_rect)
            
            # Item text
            font = pygame.font.Font(None, 32)
            name_text = font.render(item.name, True, BLACK)
            cost_text = font.render(f"Cost: {item.cost}", True, BLACK)
            desc_text = font.render(item.description, True, BLACK)
            
            screen.blit(name_text, (item_rect.x + 10, item_rect.y + 10))
            screen.blit(cost_text, (item_rect.x + 10, item_rect.y + 30))
            screen.blit(desc_text, (item_rect.x + 10, item_rect.y + 50))
            
        # Draw refresh button
        refresh_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT - 100,
            200,
            50
        )
        pygame.draw.rect(screen, WHITE, refresh_rect)
        refresh_text = pygame.font.Font(None, 32).render(
            f"Refresh ({self.refresh_cost})", True, BLACK
        )
        screen.blit(refresh_text, (refresh_rect.centerx - refresh_text.get_width()//2,
                                 refresh_rect.centery - refresh_text.get_height()//2))
                                 
    def purchase_selected_item(self, player):
        """Attempt to purchase the selected item"""
        if self.selected_item and player.money >= self.selected_item.cost:
            # Apply item effect
            stat, value = self.selected_item.effect
            player.modify_stat(stat, 1 + value)
            
            # Deduct cost
            player.money -= self.selected_item.cost
            
            # Remove item from shop
            self.items.remove(self.selected_item)
            self.selected_item = None
            return True
        return False 