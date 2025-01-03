import pygame
from game.settings import *

class HUD:
    def __init__(self):
        # Fonts
        self.title_font = pygame.font.Font(None, UI_TITLE_SIZE)
        self.text_font = pygame.font.Font(None, UI_TEXT_SIZE)
        self.small_font = pygame.font.Font(None, UI_SMALL_TEXT_SIZE)
        
        # Stats panel dimensions
        self.stats_width = 250
        self.stats_height = 120
        self.stats_padding = 10
        
        # Round info panel dimensions
        self.round_width = 200
        self.round_height = 100
        
    def draw(self, screen, player, score, current_round, round_timer):
        self._draw_stats_panel(screen, player)
        self._draw_round_panel(screen, current_round, round_timer)
        self._draw_score(screen, score)
        
    def _draw_stats_panel(self, screen, player):
        # Stats panel in top left
        panel_rect = pygame.Rect(10, 10, self.stats_width, self.stats_height)
        pygame.draw.rect(screen, UI_PANEL_COLOR, panel_rect)
        pygame.draw.rect(screen, UI_BORDER_COLOR, panel_rect, 2)
        
        # Health bar
        health_rect = pygame.Rect(20, 20, self.stats_width - 20, 20)
        pygame.draw.rect(screen, RED, health_rect)
        health_width = (player.health / player.max_health) * (self.stats_width - 20)
        pygame.draw.rect(screen, GREEN, (20, 20, health_width, 20))
        
        # Health text
        health_text = self.text_font.render(f"{int(player.health)}/{int(player.max_health)}", True, WHITE)
        health_text_rect = health_text.get_rect(center=health_rect.center)
        screen.blit(health_text, health_text_rect)
        
        # Money
        money_text = self.text_font.render(f"${player.money}", True, GOLD)
        screen.blit(money_text, (20, 50))
        
        # Stats
        stats_y = 80
        stats_text = f"DMG: {int(player.get_stat('damage'))} | SPD: {player.get_stat('move_speed'):.1f} | DEF: {int(player.get_stat('defense'))}"
        stats_surface = self.small_font.render(stats_text, True, UI_TEXT_COLOR)
        screen.blit(stats_surface, (20, stats_y))
        
    def _draw_round_panel(self, screen, current_round, round_timer):
        # Round panel in top right
        panel_rect = pygame.Rect(SCREEN_WIDTH - self.round_width - 10, 10, 
                               self.round_width, self.round_height)
        pygame.draw.rect(screen, UI_PANEL_COLOR, panel_rect)
        pygame.draw.rect(screen, UI_BORDER_COLOR, panel_rect, 2)
        
        # Round number
        round_text = self.text_font.render(f"Round {current_round}", True, WHITE)
        round_rect = round_text.get_rect(centerx=panel_rect.centerx, top=panel_rect.top + 10)
        screen.blit(round_text, round_rect)
        
        # Timer
        time_left = round_timer // FPS
        minutes = time_left // 60
        seconds = time_left % 60
        timer_text = self.title_font.render(f"{minutes:02d}:{seconds:02d}", True, WHITE)
        timer_rect = timer_text.get_rect(centerx=panel_rect.centerx, top=round_rect.bottom + 10)
        screen.blit(timer_text, timer_rect)
        
        # Timer bar
        bar_width = self.round_width - 20
        bar_height = 8
        bar_x = panel_rect.left + 10
        bar_y = panel_rect.bottom - 20
        
        pygame.draw.rect(screen, UI_ELEMENT_COLOR, (bar_x, bar_y, bar_width, bar_height))
        progress = round_timer / ROUND_DURATION
        progress_width = bar_width * progress
        pygame.draw.rect(screen, GOLD, (bar_x, bar_y, progress_width, bar_height))
        
    def _draw_score(self, screen, score):
        # Score in top center
        score_text = self.title_font.render(str(score), True, WHITE)
        score_rect = score_text.get_rect(centerx=SCREEN_WIDTH/2, top=10)
        
        # Score background
        bg_rect = score_rect.copy()
        bg_rect.inflate_ip(40, 20)
        pygame.draw.rect(screen, UI_PANEL_COLOR, bg_rect)
        pygame.draw.rect(screen, UI_BORDER_COLOR, bg_rect, 2)
        
        screen.blit(score_text, score_rect) 