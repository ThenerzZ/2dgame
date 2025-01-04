import pygame
import random
from game.settings import *
from items.item_pool import ITEM_POOL

class Shop:
    def __init__(self):
        # Colors
        self.panel_color = UI_COLORS["PANEL"]
        self.border_color = UI_COLORS["BORDER"]
        self.text_color = UI_COLORS["TEXT"]
        self.highlight_color = UI_COLORS["ACCENT"]
        
        # Dimensions
        self.width = SCREEN_WIDTH * 0.8
        self.height = SCREEN_HEIGHT * 0.8
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2
        
        # Item slots
        self.slot_size = 80
        self.slot_padding = 20
        self.slots = []
        self.selected_item = None
        self.items = []  # List to store actual items
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, UI_TITLE_SIZE)
        self.text_font = pygame.font.Font(None, UI_TEXT_SIZE)
        self.desc_font = pygame.font.Font(None, UI_SMALL_TEXT_SIZE)
        
        # Animation variables
        self.animation_time = 0
        self.hover_scale = 1.0
        
        # Create item slots and initial items
        self.create_item_slots()
        self.refresh_items()
        
    def create_item_slots(self):
        """Create item slot rectangles"""
        slots_per_row = 4
        start_x = self.x + (self.width - (slots_per_row * (self.slot_size + self.slot_padding))) // 2
        start_y = self.y + 100  # Leave space for title
        
        for i in range(SHOP_ITEMS_DISPLAYED):
            row = i // slots_per_row
            col = i % slots_per_row
            x = start_x + col * (self.slot_size + self.slot_padding)
            y = start_y + row * (self.slot_size + self.slot_padding)
            self.slots.append(pygame.Rect(x, y, self.slot_size, self.slot_size))
            
    def draw(self, screen):
        # Update animation time
        self.animation_time += 1
        
        # Get actual screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Recalculate dimensions based on actual screen size
        self.width = screen_width * 0.8
        self.height = screen_height * 0.8
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        
        # Draw main panel with border
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Draw panel shadow
        shadow_offset = 5
        shadow_rect = panel_rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        pygame.draw.rect(screen, (*UI_COLORS["BACKGROUND"], 128), shadow_rect, border_radius=10)
        
        # Draw main panel
        pygame.draw.rect(screen, self.panel_color, panel_rect, border_radius=10)
        pygame.draw.rect(screen, self.border_color, panel_rect, 2, border_radius=10)
        
        # Draw decorative corners
        corner_size = 20
        for corner in [(self.x, self.y), (self.x + self.width, self.y),
                      (self.x, self.y + self.height), (self.x + self.width, self.y + self.height)]:
            pygame.draw.line(screen, self.highlight_color,
                           (corner[0] - corner_size, corner[1]),
                           (corner[0] + corner_size, corner[1]), 2)
            pygame.draw.line(screen, self.highlight_color,
                           (corner[0], corner[1] - corner_size),
                           (corner[0], corner[1] + corner_size), 2)
        
        # Draw title
        title_text = self.title_font.render("Shop", True, self.highlight_color)
        title_rect = title_text.get_rect(centerx=self.x + self.width//2, top=self.y + 20)
        
        # Add glow effect to title
        glow_surf = pygame.Surface((title_text.get_width() + 20, title_text.get_height() + 20), pygame.SRCALPHA)
        for radius in range(10, 0, -2):
            color = (*UI_COLORS["ACCENT"][:3], 5)
            pygame.draw.rect(glow_surf, color, 
                           (10-radius, 10-radius, 
                            title_text.get_width() + radius*2, 
                            title_text.get_height() + radius*2),
                           border_radius=radius)
        screen.blit(glow_surf, (title_rect.x - 10, title_rect.y - 10))
        screen.blit(title_text, title_rect)
        
        # Recreate item slots with new dimensions
        self.create_item_slots()
        
        # Draw item slots and items
        for i, (slot, item) in enumerate(zip(self.slots, self.items)):
            # Draw slot background
            pygame.draw.rect(screen, UI_COLORS["PANEL_LIGHT"], slot, border_radius=5)
            
            # Draw slot border (highlighted if selected)
            border_color = self.highlight_color if i == self.selected_item else self.border_color
            pygame.draw.rect(screen, border_color, slot, 2, border_radius=5)
            
            # Draw item
            if item:
                # Draw item name
                name_text = self.text_font.render(item.name, True, ITEM_RARITY_COLORS[item.rarity.name])
                name_rect = name_text.get_rect(centerx=slot.centerx, bottom=slot.bottom - 5)
                screen.blit(name_text, name_rect)
                
                # Draw item cost
                cost_text = self.text_font.render(f"{item.cost}g", True, UI_COLORS["GOLD"])
                cost_rect = cost_text.get_rect(centerx=slot.centerx, top=slot.top + 5)
                screen.blit(cost_text, cost_rect)
                
                # Draw item icon or representation
                icon_rect = pygame.Rect(slot.centerx - 20, slot.centery - 20, 40, 40)
                pygame.draw.rect(screen, ITEM_RARITY_COLORS[item.rarity.name], icon_rect)
                
                # Draw hover effect and description for selected item
                if i == self.selected_item:
                    hover_rect = slot.inflate(4, 4)
                    for offset in range(3, 0, -1):
                        color = (*UI_COLORS["ACCENT"][:3], 50)
                        pygame.draw.rect(screen, color, hover_rect.inflate(offset*2, offset*2),
                                       1, border_radius=6)
                    
                    # Draw item description
                    desc_text = self.desc_font.render(item.description, True, self.text_color)
                    desc_rect = desc_text.get_rect(
                        centerx=self.x + self.width//2,
                        top=slot.bottom + 20
                    )
                    screen.blit(desc_text, desc_rect)
        
        # Draw money
        if hasattr(self, 'player'):
            money_text = self.text_font.render(f"Gold: {self.player.money}", True, UI_COLORS["GOLD"])
            screen.blit(money_text, (self.x + 20, self.y + self.height - 40))
            
        # Draw refresh cost
        refresh_text = self.text_font.render(f"Refresh ({SHOP_REFRESH_COST} gold)", True, self.text_color)
        screen.blit(refresh_text, (self.x + self.width - refresh_text.get_width() - 20,
                                 self.y + self.height - 40))
        
    def set_player(self, player):
        self.player = player
        
    def refresh_items(self):
        """Generate new items for the shop"""
        self.items = []
        available_items = ITEM_POOL.copy()
        
        # Select random items based on rarity weights
        for _ in range(SHOP_ITEMS_DISPLAYED):
            if not available_items:
                break
                
            # Calculate total weight
            total_weight = sum(ITEM_RARITY[item.rarity.name] for item in available_items)
            roll = random.random() * total_weight
            
            # Select item based on weight
            current_weight = 0
            selected_item = None
            
            for item in available_items:
                current_weight += ITEM_RARITY[item.rarity.name]
                if roll <= current_weight:
                    selected_item = item
                    break
            
            if selected_item:
                self.items.append(selected_item)
                available_items.remove(selected_item)
        
    def purchase_selected_item(self, player):
        """Handle item purchase"""
        if self.selected_item is not None and self.selected_item < len(self.items):
            item = self.items[self.selected_item]
            if player.money >= item.cost:
                player.money -= item.cost
                player.equip_item(item)
                self.items.pop(self.selected_item)
                return True
        return False
        
    def update(self):
        """Update shop state"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Update selected item based on mouse position
        self.selected_item = None
        for i, slot in enumerate(self.slots):
            if slot.collidepoint(mouse_pos):
                self.selected_item = i
                break 