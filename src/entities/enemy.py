import pygame
import random
import math
from game.settings import *
from graphics.monster_generator import MonsterGenerator

class Enemy:
    def __init__(self, monster_type=None):
        # Monster type and stats
        self.monster_type = monster_type if monster_type is not None else random.randint(0, 4)
        self.stats = self._get_monster_stats()
        
        # Generate sprite
        self.monster_gen = MonsterGenerator(size=32)
        self.sprite = self.monster_gen.generate_monster(self.monster_type)
        
        # Spawn position
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
        self.color = RED  # Fallback if no sprite
        self.facing_left = False
        
        # Health and stats
        self.max_health = self.stats["health"]
        self.health = self.max_health
        self.damage = self.stats["damage"]
        self.speed = self.stats["speed"]
        self.is_dead = False
        
        # Special effects
        self.alpha = 255
        self.has_special_movement = self.stats.get("special_movement", False)
        self.special_timer = 0
        
    def _get_monster_stats(self):
        """Get stats based on monster type"""
        base_stats = {
            0: {  # Skeleton
                "health": 60,
                "damage": 15,
                "speed": 2,
                "description": "Undead warrior, tough but slow"
            },
            1: {  # Slime
                "health": 40,
                "damage": 10,
                "speed": 1.5,
                "special_movement": "bounce",
                "description": "Gelatinous creature, bounces around"
            },
            2: {  # Spider
                "health": 30,
                "damage": 20,
                "speed": 3,
                "description": "Fast and aggressive arachnid"
            },
            3: {  # Demon
                "health": 100,
                "damage": 25,
                "speed": 2.5,
                "special_movement": "teleport",
                "description": "Powerful demon with teleportation"
            },
            4: {  # Ghost
                "health": 50,
                "damage": 15,
                "speed": 2,
                "special_movement": "phase",
                "alpha": 180,
                "description": "Ethereal spirit that phases through terrain"
            }
        }
        return base_stats[self.monster_type]

    def update(self, player_pos):
        if self.is_dead:
            return
            
        # Update special effects
        if self.has_special_movement:
            self.special_timer += 1
            if self.monster_type == 1:  # Slime bounce
                if self.special_timer % 30 == 0:  # Every half second
                    self.speed = self.stats["speed"] * (1.5 if self.speed == self.stats["speed"] else 1)
            elif self.monster_type == 3:  # Demon teleport
                if self.special_timer % 180 == 0:  # Every 3 seconds
                    self._teleport_towards(player_pos)
                    return
            elif self.monster_type == 4:  # Ghost phase
                self.alpha = 180 + math.sin(self.special_timer * 0.1) * 75
            
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

    def draw(self, screen):
        if self.is_dead:
            return
            
        # Draw sprite with special effects
        if self.sprite:
            sprite = pygame.transform.flip(self.sprite, self.facing_left, False)
            if self.monster_type == 4:  # Ghost
                # Create a copy of the sprite with current alpha
                ghost_sprite = sprite.copy()
                ghost_sprite.set_alpha(self.alpha)
                screen.blit(ghost_sprite, self.rect)
            else:
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