import pygame
from entities.player import Player
from entities.enemy import Enemy
from shop.shop import Shop
from ui.start_menu import StartMenu
from game.settings import *

class GameState:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.shop = Shop()
        self.start_menu = StartMenu(self.shop, self.player)
        self.score = 0
        self.game_over = False
        self.round_started = False  # Track if the round has started
        
        # Give initial money for start menu purchases
        self.player.money = 100  # Starting money for items

    def spawn_initial_enemies(self):
        """Spawn initial enemies when round starts"""
        self.enemies.clear()
        for _ in range(STARTING_ENEMIES):
            self.enemies.append(Enemy())

    def update(self):
        if not self.round_started:
            # Update start menu
            self.start_menu.update()
            if self.start_menu.should_start_round:
                self.round_started = True
                self.spawn_initial_enemies()
        elif not self.game_over:
            self.player.update()
            
            # Update enemies and handle combat
            self.update_enemies()
            self.handle_combat()
            
            # Remove dead enemies and spawn new ones
            self.enemies = [e for e in self.enemies if not e.is_dead]
            if len(self.enemies) < STARTING_ENEMIES:
                self.enemies.append(Enemy())

    def update_enemies(self):
        """Update all enemies"""
        for enemy in self.enemies:
            enemy.update(self.player.rect.center)

    def handle_combat(self):
        """Handle combat between player and enemies"""
        # Find closest enemy in range for auto-attack
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in self.enemies:
            if self.player.can_attack_enemy(enemy):
                dx = enemy.rect.centerx - self.player.rect.centerx
                dy = enemy.rect.centery - self.player.rect.centery
                distance = (dx * dx + dy * dy) ** 0.5
                
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
        
        # Auto-attack the closest enemy
        if closest_enemy:
            damage = self.player.attack()
            if damage > 0:  # If attack is ready
                if closest_enemy.take_damage(damage):
                    self.score += 1
                    self.player.add_money(ENEMY_KILL_REWARD)
        
        # Check for enemy attacks
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                if self.player.take_damage(enemy.damage):
                    self.game_over = True

    def draw(self, screen):
        if not self.round_started:
            # Draw start menu
            self.start_menu.draw(screen)
        else:
            # Draw game
            self.player.draw(screen)
            for enemy in self.enemies:
                enemy.draw(screen)
            
            # Draw HUD
            self.draw_hud(screen)
            
            if self.game_over:
                self.draw_game_over(screen)

    def draw_hud(self, screen):
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw money
        money_text = font.render(f'Money: ${self.player.money}', True, GOLD)
        screen.blit(money_text, (10, 50))
        
        # Draw health
        health_text = font.render(f'Health: {int(self.player.health)}/{int(self.player.max_health)}', True, GREEN)
        screen.blit(health_text, (10, 90))

    def draw_game_over(self, screen):
        font = pygame.font.Font(None, 72)
        game_over_text = font.render('Game Over!', True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(game_over_text, text_rect) 