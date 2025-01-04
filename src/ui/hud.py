import pygame
from game.settings import *

class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, UI_TEXT_SIZE)
        self.title_font = pygame.font.Font(None, UI_TITLE_SIZE)
        
        # Panel dimensions
        self.stats_panel_width = 200
        self.stats_panel_height = 120
        self.stats_panel_padding = 10
        
    def draw(self, screen, player, score, current_round, round_timer):
        self._draw_stats_panel(screen, player)
        self._draw_round_info(screen, score, current_round, round_timer)
        
    def _draw_stats_panel(self, screen, player):
        # Draw stats panel background
        panel_rect = pygame.Rect(
            self.stats_panel_padding,
            self.stats_panel_padding,
            self.stats_panel_width,
            self.stats_panel_height
        )
        pygame.draw.rect(screen, UI_COLORS["PANEL"], panel_rect)
        pygame.draw.rect(screen, UI_COLORS["BORDER"], panel_rect, 2)
        
        # Draw health bar
        health_rect = pygame.Rect(
            panel_rect.x + 10,
            panel_rect.y + 10,
            180,
            20
        )
        health_percent = player.health / player.max_health
        
        # Health bar background
        pygame.draw.rect(screen, UI_COLORS["PANEL_LIGHT"], health_rect)
        
        # Health bar fill
        if health_percent > 0:
            fill_rect = health_rect.copy()
            fill_rect.width = int(fill_rect.width * health_percent)
            pygame.draw.rect(screen, UI_COLORS["HEALTH"], fill_rect)
        
        # Health bar border
        pygame.draw.rect(screen, UI_COLORS["BORDER"], health_rect, 2)
        
        # Health text
        health_text = self.font.render(
            f"{int(player.health)}/{int(player.max_health)}", 
            True, 
            UI_COLORS["TEXT"]
        )
        health_text_rect = health_text.get_rect(
            center=(health_rect.centerx, health_rect.centery)
        )
        screen.blit(health_text, health_text_rect)
        
        # Draw money
        money_text = self.font.render(
            f"Gold: {player.money}", 
            True, 
            UI_COLORS["GOLD"]
        )
        screen.blit(money_text, (panel_rect.x + 10, panel_rect.bottom - 30))
        
    def _draw_round_info(self, screen, score, current_round, round_timer):
        # Draw round info at the top center
        round_text = self.title_font.render(
            f"Round {current_round}", 
            True, 
            UI_COLORS["ACCENT"]
        )
        round_rect = round_text.get_rect(
            midtop=(SCREEN_WIDTH // 2, 10)
        )
        screen.blit(round_text, round_rect)
        
        # Draw timer below round number
        timer_text = self.font.render(
            f"Time: {round_timer // FPS}s", 
            True, 
            UI_COLORS["TEXT"]
        )
        timer_rect = timer_text.get_rect(
            midtop=(SCREEN_WIDTH // 2, round_rect.bottom + 5)
        )
        screen.blit(timer_text, timer_rect)
        
        # Draw score in top right
        score_text = self.font.render(
            f"Score: {score}", 
            True, 
            UI_COLORS["TEXT"]
        )
        score_rect = score_text.get_rect(
            topright=(SCREEN_WIDTH - 10, 10)
        )
        screen.blit(score_text, score_rect) 