import pygame
from game.settings import *

class StartMenu:
    def __init__(self, shop, player):
        self.shop = shop
        self.player = player
        self.should_start_round = False
        
        # Button dimensions
        self.button_width = 200
        self.button_height = 50
        self.button_spacing = 20
        
        # Create buttons
        self.buttons = {
            'start': pygame.Rect(
                SCREEN_WIDTH//2 - self.button_width//2,
                SCREEN_HEIGHT//2 - self.button_height,
                self.button_width,
                self.button_height
            ),
            'shop': pygame.Rect(
                SCREEN_WIDTH//2 - self.button_width//2,
                SCREEN_HEIGHT//2 + self.button_spacing,
                self.button_width,
                self.button_height
            )
        }
        
        # Menu state
        self.in_shop = False
        
    def update(self):
        """Update menu state"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        if mouse_clicked:
            if not self.in_shop:
                # Check start button
                if self.buttons['start'].collidepoint(mouse_pos):
                    self.should_start_round = True
                # Check shop button
                elif self.buttons['shop'].collidepoint(mouse_pos):
                    self.in_shop = True
                    self.shop.refresh_items()
            else:
                # Update shop when in shop view
                self.shop.update()
                
                # Add back button functionality
                back_rect = pygame.Rect(10, 10, 100, 40)
                if back_rect.collidepoint(mouse_pos):
                    self.in_shop = False
        
    def draw(self, screen):
        """Draw menu interface"""
        if not self.in_shop:
            # Draw title
            font = pygame.font.Font(None, 72)
            title = font.render('2D Game', True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
            screen.blit(title, title_rect)
            
            # Draw buttons
            button_font = pygame.font.Font(None, 36)
            
            # Start button
            pygame.draw.rect(screen, WHITE, self.buttons['start'])
            start_text = button_font.render('Start Game', True, BLACK)
            start_rect = start_text.get_rect(center=self.buttons['start'].center)
            screen.blit(start_text, start_rect)
            
            # Shop button
            pygame.draw.rect(screen, WHITE, self.buttons['shop'])
            shop_text = button_font.render('Shop', True, BLACK)
            shop_rect = shop_text.get_rect(center=self.buttons['shop'].center)
            screen.blit(shop_text, shop_rect)
            
            # Draw player stats
            stats_font = pygame.font.Font(None, 24)
            stats_text = [
                f"Health: {self.player.max_health}",
                f"Damage: {self.player.get_stat('damage')}",
                f"Attack Speed: {self.player.get_stat('attack_speed')}",
                f"Move Speed: {self.player.get_stat('move_speed')}",
                f"Defense: {self.player.get_stat('defense')}",
                f"Money: ${self.player.money}"
            ]
            
            for i, text in enumerate(stats_text):
                stat = stats_font.render(text, True, WHITE)
                screen.blit(stat, (20, 20 + i * 25))
        else:
            # Draw shop interface
            self.shop.draw(screen)
            
            # Draw back button
            back_rect = pygame.Rect(10, 10, 100, 40)
            pygame.draw.rect(screen, WHITE, back_rect)
            back_text = pygame.font.Font(None, 32).render('Back', True, BLACK)
            back_rect_center = back_text.get_rect(center=back_rect.center)
            screen.blit(back_text, back_rect_center) 