import pygame
import math
import random
from game.settings import *
from items.inventory import Inventory
from graphics.animation_handler import AnimationHandler

class Player:
    def __init__(self, character_sprite=None):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 
                              PLAYER_SIZE, PLAYER_SIZE)
        self.sprite = character_sprite
        self.color = GREEN  # Fallback if no sprite
        self.speed = PLAYER_SPEED
        self.direction = pygame.math.Vector2()
        self.facing_left = False
        
        # Animation system
        if self.sprite:
            self.animator = AnimationHandler(self.sprite)
        else:
            self.animator = None
        
        # New attributes for items and stats
        self.inventory = Inventory()
        self.inventory.set_player(self)
        self.money = PLAYER_START_MONEY
        self.health = PLAYER_START_HEALTH
        self.max_health = PLAYER_START_HEALTH
        
        # Base stats (can be modified by items)
        self.stats = PLAYER_BASE_STATS.copy()
        
        # Stat multipliers from items
        self.stat_multipliers = {stat: 1.0 for stat in self.stats.keys()}
        
        # Attack cooldown
        self.attack_cooldown = 0
        self.attack_timer = 0
        
        # Attack animation
        self.is_attacking = False
        self.attack_animation_timer = 0
        self.attack_animation_duration = 5

    def input(self):
        keys = pygame.key.get_pressed()
        
        # Movement input
        self.direction.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_left = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_left = False
            
        self.direction.y = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            
        # Normalize diagonal movement
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
            
        # Update animation state based on movement
        if self.animator:
            if self.is_attacking:
                self.animator.set_animation('attack')
            elif self.direction.magnitude() > 0:
                self.animator.set_animation('walk')
            else:
                self.animator.set_animation('idle')

    def move(self):
        # Update position using modified speed
        actual_speed = self.get_stat("move_speed")
        self.rect.x += self.direction.x * actual_speed
        self.rect.y += self.direction.y * actual_speed
        
        # Keep player on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def update(self):
        self.input()
        self.move()
        
        # Update attack cooldown
        if self.attack_timer > 0:
            self.attack_timer -= 1
            
        # Update attack animation
        if self.attack_animation_timer > 0:
            self.attack_animation_timer -= 1
        else:
            self.is_attacking = False
            
        # Update animation frames
        if self.animator:
            self.animator.update()
        
    def draw(self, screen):
        # Draw character sprite with animations or fallback to rectangle
        if self.animator:
            current_frame = self.animator.get_current_frame()
            sprite = pygame.transform.flip(current_frame, self.facing_left, False)
            screen.blit(sprite, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw attack range indicator (semi-transparent circle)
        range_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Draw attack range with pulsing effect when attacking
        range_color = (0, 255, 0, 30)
        if self.is_attacking:
            # Make the circle pulse when attacking
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 50 + 30
            range_color = (0, 255, 0, int(pulse))
            
        pygame.draw.circle(range_surface, range_color, self.rect.center, self.get_stat("attack_range"))
        screen.blit(range_surface, (0, 0))
        
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 50
        bar_height = 5
        bar_pos = (self.rect.centerx - bar_width/2, self.rect.top - 10)
        
        # Background (red)
        pygame.draw.rect(screen, RED, (*bar_pos, bar_width, bar_height))
        # Health (green)
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, GREEN, (*bar_pos, health_width, bar_height))
        
    def get_stat(self, stat_name):
        """Get a stat's current value including item modifiers"""
        base_value = self.stats.get(stat_name, 0)
        multiplier = self.stat_multipliers.get(stat_name, 1.0)
        return base_value * multiplier
        
    def modify_stat(self, stat_name, multiplier):
        """Modify a stat's multiplier (used by items)"""
        if stat_name in self.stat_multipliers:
            self.stat_multipliers[stat_name] *= multiplier
            
    def take_damage(self, amount):
        """Take damage with defense calculation"""
        defense_multiplier = 1 - (self.get_stat("defense") / 100)
        actual_damage = max(1, amount * defense_multiplier)
        self.health = max(0, self.health - actual_damage)
        return self.health <= 0

    def heal(self, amount):
        """Heal the player"""
        self.health = min(self.max_health, self.health + amount)
        
    def add_money(self, amount):
        """Add money to the player"""
        self.money += amount
        
    def attack(self):
        """Initiate an attack"""
        if self.attack_timer <= 0:
            self.attack_timer = 60 / self.get_stat("attack_speed")  # 60 frames per second
            self.is_attacking = True
            self.attack_animation_timer = self.attack_animation_duration
            return self.calculate_damage()
        return 0
        
    def calculate_damage(self):
        """Calculate damage with critical hits"""
        base_damage = self.get_stat("damage")
        
        # Check for critical hit
        if random.random() < self.get_stat("crit_chance"):
            return base_damage * self.get_stat("crit_damage")
        return base_damage
        
    def can_attack_enemy(self, enemy):
        """Check if an enemy is within attack range"""
        if enemy.is_dead:
            return False
        dx = enemy.rect.centerx - self.rect.centerx
        dy = enemy.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        return distance <= self.get_stat("attack_range") 