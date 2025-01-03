import pygame
from game.settings import *
from items.item_pool import ITEM_POOL

class StartMenu:
    def __init__(self, shop, player):
        self.shop = shop
        self.player = player
        self.should_start_round = False
        
        # UI elements
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        
        # Button rectangles
        button_width = 200
        button_height = 50
        center_x = SCREEN_WIDTH // 2
        self.start_button = pygame.Rect(
            center_x - button_width//2,
            SCREEN_HEIGHT - 100,
            button_width,
            button_height
        )
        
        # Shop items display
        self.item_rects = []
        self.refresh_button = pygame.Rect(
            SCREEN_WIDTH - 150,
            50,
            120,
            40
        )
        
        # Initialize shop items
        self.shop.generate_items(ITEM_POOL)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        if mouse_clicked:
            # Check start button
            if self.start_button.collidepoint(mouse_pos):
                self.should_start_round = True
                
            # Check refresh button
            if self.refresh_button.collidepoint(mouse_pos):
                self.shop.refresh_shop(self.player, ITEM_POOL)
                
            # Check item clicks
            for i, item_rect in enumerate(self.item_rects):
                if item_rect.collidepoint(mouse_pos):
                    self.shop.purchase_item(self.player, i)

    def draw(self, screen):
        # Draw background
        screen.fill(BLACK)
        
        # Draw title
        title = self.title_font.render("Prepare for Battle", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        screen.blit(title, title_rect)
        
        # Draw money
        money_text = self.font.render(f"Money: ${self.player.money}", True, GOLD)
        screen.blit(money_text, (20, 20))
        
        # Draw shop items
        self.item_rects.clear()
        for i, item in enumerate(self.shop.available_items):
            item_rect = pygame.Rect(
                50,
                150 + i * 100,
                SCREEN_WIDTH - 100,
                80
            )
            self.item_rects.append(item_rect)
            
            # Draw item background
            pygame.draw.rect(screen, GRAY, item_rect, border_radius=10)
            
            # Draw item info
            name_text = self.font.render(item.name, True, item.get_display_color())
            desc_text = self.font.render(item.description, True, WHITE)
            cost_text = self.font.render(f"${item.cost}", True, GOLD)
            
            screen.blit(name_text, (item_rect.x + 20, item_rect.y + 10))
            screen.blit(desc_text, (item_rect.x + 20, item_rect.y + 40))
            screen.blit(cost_text, (item_rect.right - 70, item_rect.centery - 10))
        
        # Draw refresh button
        pygame.draw.rect(screen, BLUE, self.refresh_button, border_radius=5)
        refresh_text = self.font.render(f"Refresh (${self.shop.refresh_cost})", True, WHITE)
        screen.blit(refresh_text, (self.refresh_button.x + 10, self.refresh_button.y + 10))
        
        # Draw start button
        pygame.draw.rect(screen, GREEN, self.start_button, border_radius=10)
        start_text = self.font.render("Start Round", True, BLACK)
        text_rect = start_text.get_rect(center=self.start_button.center)
        screen.blit(start_text, text_rect) 