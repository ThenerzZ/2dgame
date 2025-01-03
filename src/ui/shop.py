import pygame
import random
from game.settings import *
from items.item_pool import ITEM_POOL

class Shop:
    def __init__(self):
        self.items = []
        self.selected_item = None
        
        # UI constants
        self.PANEL_COLOR = UI_PANEL_COLOR
        self.ITEM_COLOR = UI_ELEMENT_COLOR
        self.SELECTED_COLOR = UI_SELECTED_COLOR
        self.HOVER_COLOR = UI_HOVER_COLOR
        self.BORDER_COLOR = UI_BORDER_COLOR
        
        # Shop panel dimensions
        self.panel_width = SCREEN_WIDTH * 0.8
        self.panel_height = SCREEN_HEIGHT * 0.8
        self.panel_x = (SCREEN_WIDTH - self.panel_width) / 2
        self.panel_y = (SCREEN_HEIGHT - self.panel_height) / 2
        
        # Item slot dimensions
        self.item_width = self.panel_width * 0.4
        self.item_height = 120
        self.item_padding = 20
        
        # Button dimensions
        self.button_width = 200
        self.button_height = 40
        
        # Fonts
        self.title_font = pygame.font.Font(None, UI_TITLE_SIZE)
        self.item_font = pygame.font.Font(None, UI_TEXT_SIZE)
        self.desc_font = pygame.font.Font(None, UI_SMALL_TEXT_SIZE)
        
        self.refresh_items()
        
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
        """Attempt to purchase the selected item"""
        if not self.selected_item:
            return False
            
        if player.money >= self.selected_item.cost:
            player.money -= self.selected_item.cost
            player.equip_item(self.selected_item)  # Use new equip system
            self.items.remove(self.selected_item)
            self.selected_item = None
            return True
            
        return False
        
    def draw(self, screen):
        # Draw semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Draw main panel
        panel_rect = pygame.Rect(self.panel_x, self.panel_y, self.panel_width, self.panel_height)
        pygame.draw.rect(screen, self.PANEL_COLOR, panel_rect)
        pygame.draw.rect(screen, self.BORDER_COLOR, panel_rect, 2)
        
        # Draw title
        title = self.title_font.render("SHOP", True, WHITE)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH/2, top=self.panel_y + 20)
        screen.blit(title, title_rect)
        
        # Draw player stats
        stats_text = self.item_font.render(f"Money: ${self.player.money}", True, GOLD)
        stats_rect = stats_text.get_rect(right=self.panel_x + self.panel_width - 20, top=self.panel_y + 20)
        screen.blit(stats_text, stats_rect)
        
        health_text = self.item_font.render(f"Health: {int(self.player.health)}/{int(self.player.max_health)}", True, GREEN)
        health_rect = health_text.get_rect(right=stats_rect.left - 20, top=self.panel_y + 20)
        screen.blit(health_text, health_rect)
        
        # Draw items
        mouse_pos = pygame.mouse.get_pos()
        start_y = self.panel_y + 80
        
        for i, item in enumerate(self.items):
            item_x = self.panel_x + (20 if i < 2 else self.panel_width/2 + 20)
            item_y = start_y + (self.item_height + self.item_padding) * (i % 2)
            
            # Item background
            item_rect = pygame.Rect(item_x, item_y, self.item_width, self.item_height)
            
            # Determine item color based on state
            if item_rect.collidepoint(mouse_pos):
                color = self.HOVER_COLOR
            elif item == self.selected_item:
                color = self.SELECTED_COLOR
            else:
                color = self.ITEM_COLOR
                
            pygame.draw.rect(screen, color, item_rect)
            pygame.draw.rect(screen, self.BORDER_COLOR, item_rect, 2)
            
            # Draw item name with rarity color
            name_color = ITEM_RARITY_COLORS.get(item.rarity.name, WHITE)
            name_text = self.item_font.render(item.name, True, name_color)
            screen.blit(name_text, (item_x + 10, item_y + 10))
            
            # Draw item type indicator
            type_text = self.desc_font.render(f"[{item.item_type.name}]", True, WHITE)
            type_rect = type_text.get_rect(left=item_x + name_text.get_width() + 20, top=item_y + 13)
            screen.blit(type_text, type_rect)
            
            # Draw item cost
            cost_text = self.item_font.render(f"${item.cost}", True, GOLD)
            cost_rect = cost_text.get_rect(right=item_rect.right - 10, top=item_y + 10)
            screen.blit(cost_text, cost_rect)
            
            # Draw item description
            desc_lines = self.wrap_text(item.description, self.desc_font, self.item_width - 20)
            for j, line in enumerate(desc_lines):
                desc_text = self.desc_font.render(line, True, WHITE)
                screen.blit(desc_text, (item_x + 10, item_y + 45 + j * 20))
                
            # Draw "Can't afford" overlay if applicable
            if item.cost > self.player.money:
                cant_afford = pygame.Surface((self.item_width, self.item_height))
                cant_afford.fill((200, 0, 0))
                cant_afford.set_alpha(64)
                screen.blit(cant_afford, item_rect)
                
        # Draw refresh button
        refresh_rect = pygame.Rect(
            SCREEN_WIDTH/2 - self.button_width/2,
            self.panel_y + self.panel_height - 60,
            self.button_width,
            self.button_height
        )
        
        refresh_color = self.HOVER_COLOR if refresh_rect.collidepoint(mouse_pos) else self.ITEM_COLOR
        pygame.draw.rect(screen, refresh_color, refresh_rect)
        pygame.draw.rect(screen, self.BORDER_COLOR, refresh_rect, 2)
        
        refresh_text = self.item_font.render(f"Refresh (${SHOP_REFRESH_COST})", True, WHITE)
        refresh_text_rect = refresh_text.get_rect(center=refresh_rect.center)
        screen.blit(refresh_text, refresh_text_rect)
        
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within a given width"""
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            word_surface = font.render(word + ' ', True, WHITE)
            word_width = word_surface.get_width()
            
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
                
        lines.append(' '.join(current_line))
        return lines
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        # Check item clicks
        start_y = self.panel_y + 80
        for i, item in enumerate(self.items):
            item_x = self.panel_x + (20 if i < 2 else self.panel_width/2 + 20)
            item_y = start_y + (self.item_height + self.item_padding) * (i % 2)
            item_rect = pygame.Rect(item_x, item_y, self.item_width, self.item_height)
            
            if item_rect.collidepoint(mouse_pos):
                if mouse_clicked:
                    self.selected_item = item
                    
        # Check refresh button click
        refresh_rect = pygame.Rect(
            SCREEN_WIDTH/2 - self.button_width/2,
            self.panel_y + self.panel_height - 60,
            self.button_width,
            self.button_height
        )
        
        if refresh_rect.collidepoint(mouse_pos) and mouse_clicked:
            if self.player.money >= SHOP_REFRESH_COST:
                self.player.money -= SHOP_REFRESH_COST
                self.refresh_items()
                
    def set_player(self, player):
        self.player = player 