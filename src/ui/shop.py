import pygame
import random
from game.settings import *

class Item:
    def __init__(self, name, description, cost, rarity, effect):
        self.name = name
        self.description = description
        self.cost = cost
        self.rarity = rarity
        self.effect = effect

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
        for _ in range(SHOP_ITEMS_DISPLAYED):
            self.items.append(self.generate_random_item())
            
    def generate_random_item(self):
        """Generate a random item with appropriate stats"""
        # Determine rarity
        roll = random.random() * 100
        cumulative = 0
        selected_rarity = "COMMON"
        
        for rarity, chance in ITEM_RARITY.items():
            cumulative += chance
            if roll <= cumulative:
                selected_rarity = rarity
                break
                
        # Item pools based on rarity
        items = {
            "COMMON": [
                ("Sharp Blade", "Damage +10%", 50, lambda p: p.modify_stat("damage", 1.1)),
                ("Running Shoes", "Speed +10%", 50, lambda p: p.modify_stat("move_speed", 1.1)),
                ("Leather Armor", "Defense +10%", 50, lambda p: p.modify_stat("defense", 1.1)),
            ],
            "RARE": [
                ("Enchanted Sword", "Damage +20%", 100, lambda p: p.modify_stat("damage", 1.2)),
                ("Swift Boots", "Speed +20%", 100, lambda p: p.modify_stat("move_speed", 1.2)),
                ("Steel Armor", "Defense +20%", 100, lambda p: p.modify_stat("defense", 1.2)),
                ("Quick Loader", "Attack Speed +15%", 100, lambda p: p.modify_stat("attack_speed", 1.15)),
            ],
            "EPIC": [
                ("Ancient Blade", "Damage +35%", 200, lambda p: p.modify_stat("damage", 1.35)),
                ("Hermes Boots", "Speed +35%", 200, lambda p: p.modify_stat("move_speed", 1.35)),
                ("Dragon Scale", "Defense +35%", 200, lambda p: p.modify_stat("defense", 1.35)),
                ("Critical Eye", "Crit Chance +10%", 200, lambda p: p.modify_stat("crit_chance", 1.5)),
            ],
            "LEGENDARY": [
                ("God Slayer", "Damage +50%", 300, lambda p: p.modify_stat("damage", 1.5)),
                ("Sonic Boots", "Speed +50%", 300, lambda p: p.modify_stat("move_speed", 1.5)),
                ("Holy Armor", "Defense +50%", 300, lambda p: p.modify_stat("defense", 1.5)),
                ("Death's Eye", "Crit Damage +50%", 300, lambda p: p.modify_stat("crit_damage", 1.5)),
            ]
        }
        
        # Select random item from appropriate pool
        name, desc, cost, effect = random.choice(items[selected_rarity])
        return Item(name, desc, cost, selected_rarity, effect)
        
    def purchase_selected_item(self, player):
        """Attempt to purchase the selected item"""
        if not self.selected_item:
            return False
            
        if player.money >= self.selected_item.cost:
            player.money -= self.selected_item.cost
            self.selected_item.effect(player)
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
            name_color = ITEM_RARITY_COLORS.get(item.rarity, WHITE)
            name_text = self.item_font.render(item.name, True, name_color)
            screen.blit(name_text, (item_x + 10, item_y + 10))
            
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