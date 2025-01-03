import pygame
import random
import math
from game.settings import *
from graphics.monster_generator import MonsterGenerator

class Enemy:
    def __init__(self):
        # Monster type and stats
        self.rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        self.spawn_at_edge()
        
        # Generate sprite
        self.monster_gen = MonsterGenerator(size=32)
        self.sprite = None  # Will be set when tier is assigned
        self.facing_left = False
        
        # These will be set by the tier system
        self.health = 0
        self.max_health = 0
        self.damage = 0
        self.speed = 0
        self.kill_reward = 0
        self.tier = "NORMAL"
        
        # Special effects
        self.alpha = 255
        self.has_special_movement = False
        self.special_timer = 0
        
        self.is_dead = False
        self.direction = pygame.math.Vector2()
        
    def set_monster_type(self, tier):
        """Set monster type based on tier"""
        if tier == "WEAK":
            monster_type = 1  # Slime
        elif tier == "NORMAL":
            monster_type = 0  # Skeleton
        elif tier == "STRONG":
            monster_type = 2  # Spider
        elif tier == "ELITE":
            monster_type = 3  # Demon
        else:  # BOSS
            monster_type = 4  # Ghost
            
        self.sprite = self.monster_gen.generate_monster(monster_type)
        self.has_special_movement = monster_type in [1, 3, 4]  # Slime, Demon, Ghost
        
    def draw(self, screen):
        if self.is_dead:
            return
            
        # Draw sprite with special effects
        if self.sprite:
            sprite = pygame.transform.flip(self.sprite, self.facing_left, False)
            if self.tier == "BOSS":  # Ghost-like effect for bosses
                ghost_sprite = sprite.copy()
                ghost_sprite.set_alpha(self.alpha)
                screen.blit(ghost_sprite, self.rect)
            else:
                screen.blit(sprite, self.rect)
        
        # Draw health bar
        self.draw_health_bar(screen)
        
        # Draw tier indicator (small circle above enemy)
        indicator_radius = 4
        indicator_pos = (self.rect.centerx, self.rect.top - 8)
        indicator_color = ENEMY_TIERS[self.tier]["color"]
        pygame.draw.circle(screen, indicator_color, indicator_pos, indicator_radius)
        
    def draw_health_bar(self, screen):
        bar_width = 30
        bar_height = 4
        bar_pos = (self.rect.centerx - bar_width/2, self.rect.top - 6)
        
        # Background (red)
        pygame.draw.rect(screen, RED, (*bar_pos, bar_width, bar_height))
        # Health (color based on tier)
        health_width = (self.health / self.max_health) * bar_width
        tier_color = ENEMY_TIERS[self.tier]["color"]
        pygame.draw.rect(screen, tier_color, (*bar_pos, health_width, bar_height))
        
    def update(self, player_pos):
        if not self.is_dead:
            # Update special effects
            if self.has_special_movement:
                self.special_timer += 1
                if self.tier == "WEAK":  # Slime bounce
                    if self.special_timer % 30 == 0:  # Every half second
                        self.speed = ENEMY_TIERS[self.tier]["speed"] * (1.5 if self.speed == ENEMY_TIERS[self.tier]["speed"] else 1)
                elif self.tier == "ELITE":  # Demon teleport
                    if self.special_timer % 180 == 0:  # Every 3 seconds
                        self._teleport_towards(player_pos)
                        return
                elif self.tier == "BOSS":  # Ghost phase
                    self.alpha = 180 + math.sin(self.special_timer * 0.1) * 75
            
            # Calculate direction to player
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            
            # Update facing direction
            self.facing_left = dx < 0
            
            # Normalize direction
            length = math.sqrt(dx * dx + dy * dy)
            if length > 0:
                self.direction.x = dx / length
                self.direction.y = dy / length
                
            # Move towards player
            self.rect.x += self.direction.x * self.speed
            self.rect.y += self.direction.y * self.speed
            
    def _teleport_towards(self, player_pos):
        """Teleport closer to the player (demon ability)"""
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(100, 200)
        
        target_x = player_pos[0] + math.cos(angle) * distance
        target_y = player_pos[1] + math.sin(angle) * distance
        
        # Keep within screen bounds
        target_x = max(0, min(SCREEN_WIDTH - self.rect.width, target_x))
        target_y = max(0, min(SCREEN_HEIGHT - self.rect.height, target_y))
        
        self.rect.x = target_x
        self.rect.y = target_y
        
    def take_damage(self, amount):
        """Take damage and return True if enemy died"""
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.is_dead = True
            return True
        return False
        
    def spawn_at_edge(self):
        """Spawn the enemy at a random edge of the screen"""
        side = random.randint(0, 3)
        if side == 0:  # Top
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = -self.rect.height
        elif side == 1:  # Right
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        elif side == 2:  # Bottom
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = SCREEN_HEIGHT
        else:  # Left
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height) 