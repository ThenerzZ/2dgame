import pygame
import random
from game.settings import *

class Enemy:
    def __init__(self, character_sprite=None):
        # Spawn enemy at random edge of the screen
        side = random.randint(0, 3)
        if side == 0:  # Top
            x = random.randint(0, SCREEN_WIDTH)
            y = -PLAYER_SIZE
        elif side == 1:  # Right
            x = SCREEN_WIDTH + PLAYER_SIZE
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # Bottom
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + PLAYER_SIZE
        else:  # Left
            x = -PLAYER_SIZE
            y = random.randint(0, SCREEN_HEIGHT)

        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.sprite = character_sprite
        self.color = RED  # Fallback if no sprite
        self.speed = ENEMY_BASE_STATS["speed"]
        self.facing_left = False
        
        # Health and damage
        self.max_health = ENEMY_BASE_STATS["health"]
        self.health = self.max_health
        self.damage = ENEMY_BASE_STATS["damage"]
        self.is_dead = False

    def update(self, player_pos):
        if self.is_dead:
            return
            
        # Move towards player
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        
        # Update facing direction
        self.facing_left = dx < 0
        
        # Normalize direction
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
            
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        if self.is_dead:
            return
            
        # Draw character sprite or fallback to rectangle
        if self.sprite:
            sprite = pygame.transform.flip(self.sprite, self.facing_left, False)
            screen.blit(sprite, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw health bar
        bar_width = 40
        bar_height = 4
        bar_pos = (self.rect.centerx - bar_width/2, self.rect.top - 8)
        
        # Background (red)
        pygame.draw.rect(screen, RED, (*bar_pos, bar_width, bar_height))
        # Health (green)
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, GREEN, (*bar_pos, health_width, bar_height))

    def take_damage(self, amount):
        """Take damage and return True if enemy dies"""
        self.health -= amount
        if self.health <= 0:
            self.is_dead = True
            return True
        return False 