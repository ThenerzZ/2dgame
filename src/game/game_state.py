import pygame
from entities.player import Player
from entities.enemy import Enemy
from shop.shop import Shop
from ui.start_menu import StartMenu
from graphics.terrain_generator import TerrainGenerator
from graphics.character_generator import CharacterGenerator
from game.settings import *
import random
import math

class GameState:
    def __init__(self):
        # Initialize generators
        self.terrain_gen = TerrainGenerator(tile_size=32)
        self.char_gen = CharacterGenerator(size=32)
        
        # Generate terrain
        self.terrain = self.terrain_gen.generate_chunk(
            width=SCREEN_WIDTH//32,
            height=SCREEN_HEIGHT//32,
            seed=random.randint(0, 1000)
        )
        
        # Create player with generated character sprite
        self.player = Player(character_sprite=self.char_gen.generate_character())
        self.enemies = []
        self.shop = Shop()
        self.start_menu = StartMenu(self.shop, self.player)
        self.score = 0
        self.game_over = False
        self.round_started = False
        
        # Bonfire system
        self.bonfire_cooldowns = {pos: 0 for pos in self.terrain_gen.bonfire_positions}
        
        # Give initial money for start menu purchases
        self.player.money = PLAYER_START_MONEY

    def spawn_initial_enemies(self):
        """Spawn initial enemies when round starts"""
        self.enemies.clear()
        
        # Start with basic enemies
        num_enemies = STARTING_ENEMIES
        for _ in range(num_enemies):
            # Higher chance for basic enemies at start
            weights = [0.4, 0.3, 0.2, 0.05, 0.05]  # Skeleton, Slime, Spider, Demon, Ghost
            monster_type = random.choices(range(5), weights=weights)[0]
            self.enemies.append(Enemy(monster_type=monster_type))
            
    def spawn_enemy(self):
        """Spawn a new enemy with type based on score"""
        # Adjust spawn weights based on score
        if self.score < 1000:
            weights = [0.3, 0.3, 0.2, 0.1, 0.1]  # More basic enemies
        elif self.score < 2000:
            weights = [0.2, 0.2, 0.3, 0.15, 0.15]  # More spiders
        elif self.score < 3000:
            weights = [0.15, 0.15, 0.2, 0.25, 0.25]  # More demons and ghosts
        else:
            weights = [0.1, 0.1, 0.2, 0.3, 0.3]  # Mostly tough enemies
            
        monster_type = random.choices(range(5), weights=weights)[0]
        self.enemies.append(Enemy(monster_type=monster_type))
        
    def update(self):
        if not self.round_started:
            # Update start menu
            self.start_menu.update()
            if self.start_menu.should_start_round:
                self.round_started = True
                self.spawn_initial_enemies()
        elif not self.game_over:
            # Pass enemies list to player for targeting
            self.player.current_enemies = self.enemies
            self.player.update()
            
            # Update enemies and handle combat
            self.update_enemies()
            self.handle_combat()
            
            # Update bonfire cooldowns and particles
            for pos in self.bonfire_cooldowns:
                if self.bonfire_cooldowns[pos] > 0:
                    self.bonfire_cooldowns[pos] -= 1
            
            # Update particle effects
            self.terrain_gen.update_particles()
            
            # Check for bonfire healing
            self.check_bonfire_healing()
            
            # Remove dead enemies and spawn new ones
            self.enemies = [e for e in self.enemies if not e.is_dead]
            if len(self.enemies) < STARTING_ENEMIES:
                self.spawn_enemy()  # Use new spawn method

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

    def check_bonfire_healing(self):
        """Check if player is near a bonfire and apply healing"""
        player_center = self.player.rect.center
        
        for bonfire_pos in self.terrain_gen.bonfire_positions:
            # Skip if bonfire is on cooldown
            if self.bonfire_cooldowns[bonfire_pos] > 0:
                continue
                
            # Check if player is in range
            dx = player_center[0] - bonfire_pos[0]
            dy = player_center[1] - bonfire_pos[1]
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance <= BONFIRE_HEAL_RADIUS:
                # Heal player and start cooldown
                self.player.heal(BONFIRE_HEAL_AMOUNT)
                self.bonfire_cooldowns[bonfire_pos] = BONFIRE_COOLDOWN
                # Create healing effect
                self.create_heal_effect(player_center)

    def create_heal_effect(self, position):
        """Create a visual healing effect"""
        effect_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Draw healing circles
        for radius in range(5, 20, 2):
            alpha = int(255 * (1 - radius/20))  # Fade out with distance
            pygame.draw.circle(effect_surface, (*GREEN, alpha), position, radius, 1)
            
        return effect_surface

    def draw(self, screen):
        if not self.round_started:
            # Draw start menu
            self.start_menu.draw(screen)
        else:
            # Draw terrain
            screen.blit(self.terrain, (0, 0))
            
            # Draw bonfire cooldown indicators
            for pos in self.bonfire_cooldowns:
                if self.bonfire_cooldowns[pos] > 0:
                    # Draw cooldown circle
                    progress = self.bonfire_cooldowns[pos] / BONFIRE_COOLDOWN
                    radius = BONFIRE_HEAL_RADIUS * (1 - progress)
                    pygame.draw.circle(screen, (*ORANGE, 30), pos, int(radius), 1)
            
            # Draw game entities
            self.player.draw(screen)
            for enemy in self.enemies:
                enemy.draw(screen)
                
            # Draw particle effects
            self.terrain_gen.draw_particles(screen)
            
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
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Game over text
        font = pygame.font.Font(None, 72)
        game_over_text = font.render('Game Over!', True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(game_over_text, text_rect)
        
        # Score text
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f'Final Score: {self.score}', True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60))
        screen.blit(score_text, score_rect) 