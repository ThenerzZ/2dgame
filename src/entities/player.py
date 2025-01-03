import pygame
import math
import random
from game.settings import *
from items.inventory import Inventory
from graphics.animation_handler import AnimationHandler
from graphics.bullet_particles import BulletParticleSystem
from graphics.gun_animation_handler import GunAnimationHandler
from graphics.equipment_sprites import EquipmentSprites
from items.item_base import ItemType

class Player:
    def __init__(self, character_sprite=None):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 
                              PLAYER_SIZE, PLAYER_SIZE)
        self.sprite = character_sprite
        self.color = GREEN  # Fallback if no sprite
        self.speed = PLAYER_SPEED
        self.direction = pygame.math.Vector2()
        self.facing_left = False
        
        # Equipment system
        self.equipment_sprites = EquipmentSprites(PLAYER_SIZE)
        self.equipped_weapon = None
        self.weapon_sprite = None
        self.armor_overlays = []  # List of armor visual effects
        
        # Animation system
        if self.sprite:
            self.animator = AnimationHandler(self.sprite)
            # Initialize gun animation
            gun_sprite = pygame.Surface((24, 12), pygame.SRCALPHA)  # Basic gun shape
            pygame.draw.rect(gun_sprite, (100, 100, 100), (0, 3, 20, 6))  # Gun body
            pygame.draw.rect(gun_sprite, (80, 80, 80), (16, 2, 8, 8))  # Gun barrel
            self.gun_animator = GunAnimationHandler(gun_sprite)
        else:
            self.animator = None
            self.gun_animator = None
        
        # Gun state
        self.gun_offset_x = 20
        self.gun_offset_y = 0
        self.gun_angle = 0
        self.is_shooting = False
        self.shoot_cooldown = 0
        
        # Bullet system
        self.bullet_system = BulletParticleSystem()
        
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
        
        # Temporary buffs system
        self.temporary_buffs = {}  # {stat_name: [(multiplier, remaining_time), ...]}
        
        # Attack cooldown
        self.attack_cooldown = 0
        self.attack_timer = 0
        
        # Attack animation
        self.is_attacking = False
        self.attack_animation_timer = 0
        self.attack_animation_duration = 5

    def equip_item(self, item):
        """Handle equipping an item and updating visuals"""
        if item.item_type == ItemType.ACTIVE:
            self.equipped_weapon = item
            self.weapon_sprite = self.equipment_sprites.generate_weapon_sprite(item.name)
        elif item.item_type == ItemType.PASSIVE:
            # Generate armor overlay if the item has a visual effect
            overlay = self.equipment_sprites.generate_armor_overlay(item.name)
            if overlay:
                self.armor_overlays.append(overlay)
        
        # Apply item stats
        item.apply_effect(self)

    def unequip_item(self, item):
        """Handle unequipping an item and removing visuals"""
        if item.item_type == ItemType.ACTIVE and self.equipped_weapon == item:
            self.equipped_weapon = None
            self.weapon_sprite = None
        elif item.item_type == ItemType.PASSIVE:
            # Remove armor overlay if it exists
            self.armor_overlays = [overlay for overlay in self.armor_overlays 
                                 if overlay != self.equipment_sprites.generate_armor_overlay(item.name)]
        
        # Remove item stats
        item.remove_effect(self)

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
            
        # Update shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # Update animations
        if self.animator:
            # Update character animation
            if self.is_attacking:
                self.animator.set_animation('attack')
            elif abs(self.direction.x) > 0 or abs(self.direction.y) > 0:
                self.animator.set_animation('walk')
            else:
                self.animator.set_animation('idle')
            self.animator.update()
            
            # Update gun animation
            if self.gun_animator:
                self.gun_animator.update()
                
        # Calculate gun angle based on movement or target
        if self.direction.magnitude() > 0:
            self.gun_angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
        
        # Update bullet system
        self.bullet_system.update()
        
        # Update temporary buffs
        self._update_temporary_buffs()

    def draw(self, screen):
        # Draw character sprite with animations or fallback to rectangle
        if self.animator:
            current_frame = self.animator.get_current_frame()
            sprite = pygame.transform.flip(current_frame, self.facing_left, False)
            
            # Draw base character
            screen.blit(sprite, self.rect)
            
            # Draw armor overlays
            for overlay in self.armor_overlays:
                overlay_flipped = pygame.transform.flip(overlay, self.facing_left, False)
                screen.blit(overlay_flipped, self.rect)
            
            # Draw equipped weapon
            if self.weapon_sprite:
                # Calculate weapon position and rotation
                weapon_x = self.rect.centerx + (self.gun_offset_x if not self.facing_left else -self.gun_offset_x)
                weapon_y = self.rect.centery + self.gun_offset_y
                
                # Rotate weapon
                rotated_weapon = pygame.transform.rotate(self.weapon_sprite, -self.gun_angle)
                weapon_rect = rotated_weapon.get_rect(center=(weapon_x, weapon_y))
                
                # Draw weapon
                screen.blit(rotated_weapon, weapon_rect)
                
                # Draw attack effects if attacking
                if self.is_attacking and self.equipped_weapon:
                    self._draw_attack_effects(screen, weapon_x, weapon_y)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw bullets and effects
        self.bullet_system.draw(screen)
        
        self.draw_health_bar(screen)

    def _draw_attack_effects(self, screen, weapon_x, weapon_y):
        """Draw weapon-specific attack effects"""
        if self.equipped_weapon.name == "Magic Wand":
            # Magic sparkle effect
            for _ in range(3):
                angle = self.gun_angle + random.uniform(-30, 30)
                distance = random.uniform(15, 25)
                effect_x = weapon_x + math.cos(math.radians(angle)) * distance
                effect_y = weapon_y + math.sin(math.radians(angle)) * distance
                
                pygame.draw.circle(screen, (100, 200, 255, 150), (int(effect_x), int(effect_y)), 2)
        
        elif self.equipped_weapon.name == "Fire Wand":
            # Fire trail effect
            for _ in range(5):
                angle = self.gun_angle + random.uniform(-20, 20)
                distance = random.uniform(10, 30)
                effect_x = weapon_x + math.cos(math.radians(angle)) * distance
                effect_y = weapon_y + math.sin(math.radians(angle)) * distance
                
                size = random.uniform(2, 4)
                alpha = int(255 * (1 - distance/30))
                pygame.draw.circle(screen, (255, 100, 0, alpha), 
                                 (int(effect_x), int(effect_y)), int(size))
        
        elif self.equipped_weapon.name == "Lightning Ring":
            # Lightning effect
            for _ in range(2):
                start_angle = self.gun_angle + random.uniform(-30, 30)
                points = [(weapon_x, weapon_y)]
                
                for _ in range(3):
                    angle = start_angle + random.uniform(-45, 45)
                    length = random.uniform(10, 20)
                    x = points[-1][0] + math.cos(math.radians(angle)) * length
                    y = points[-1][1] + math.sin(math.radians(angle)) * length
                    points.append((x, y))
                
                pygame.draw.lines(screen, (100, 150, 255, 180), False, points, 2)

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
        """Get a stat's current value including item modifiers and temporary buffs"""
        base_value = self.stats.get(stat_name, 0)
        permanent_multiplier = self.stat_multipliers.get(stat_name, 1.0)
        
        # Apply temporary buffs
        temp_multiplier = 1.0
        if stat_name in self.temporary_buffs:
            for mult, _ in self.temporary_buffs[stat_name]:
                temp_multiplier *= mult
                
        return base_value * permanent_multiplier * temp_multiplier
        
    def modify_stat(self, stat_name, multiplier):
        """Modify a stat's multiplier (used by items)"""
        if stat_name in self.stat_multipliers:
            self.stat_multipliers[stat_name] *= multiplier
            
    def take_damage(self, amount):
        """Take damage with defense calculation"""
        defense_multiplier = 1 - (self.get_stat("defense") / 100)
        actual_damage = max(1, amount * defense_multiplier)
        self.health = max(0, self.health - actual_damage)
        
        # Set hurt animation
        if self.animator:
            self.animator.set_animation('hurt')
            
        # Return True if player died
        return self.health <= 0

    def heal(self, amount):
        """Heal the player"""
        self.health = min(self.max_health, self.health + amount)
        
    def add_money(self, amount):
        """Add money to the player"""
        self.money += amount
        
    def attack(self):
        """Shoot at the nearest enemy"""
        if self.attack_timer <= 0 and self.shoot_cooldown <= 0:
            self.attack_timer = 60 / self.get_stat("attack_speed")  # 60 frames per second
            self.shoot_cooldown = 10  # Additional cooldown for gun animation
            self.is_attacking = True
            self.attack_animation_timer = self.attack_animation_duration
            
            # Trigger gun shoot animation
            if self.gun_animator:
                self.gun_animator.set_animation('shoot')
            
            # Calculate gun position
            gun_x = self.rect.centerx + (self.gun_offset_x if not self.facing_left else -self.gun_offset_x)
            gun_y = self.rect.centery + self.gun_offset_y
            
            # Find closest enemy position
            closest_enemy = None
            min_distance = float('inf')
            
            for enemy in self.current_enemies:
                if self.can_attack_enemy(enemy):
                    dx = enemy.rect.centerx - self.rect.centerx
                    dy = enemy.rect.centery - self.rect.centery
                    distance = math.sqrt(dx * dx + dy * dy)
                    
                    if distance < min_distance:
                        min_distance = distance
                        closest_enemy = enemy
            
            if closest_enemy:
                # Update gun angle to face target
                dx = closest_enemy.rect.centerx - gun_x
                dy = closest_enemy.rect.centery - gun_y
                self.gun_angle = math.degrees(math.atan2(dy, dx))
                
                # Create bullet effect
                target_x = closest_enemy.rect.centerx
                target_y = closest_enemy.rect.centery
                self.bullet_system.shoot((gun_x, gun_y), (target_x, target_y))
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

    def add_temporary_buff(self, stat_name, multiplier, duration):
        """Add a temporary buff to a stat"""
        if stat_name not in self.temporary_buffs:
            self.temporary_buffs[stat_name] = []
        self.temporary_buffs[stat_name].append([multiplier, duration * FPS])  # Convert duration to frames
        
    def _update_temporary_buffs(self):
        """Update all temporary buffs"""
        for stat_name in list(self.temporary_buffs.keys()):
            # Update each buff for this stat
            self.temporary_buffs[stat_name] = [
                [mult, time - 1] for mult, time in self.temporary_buffs[stat_name]
                if time > 0
            ]
            
            # Remove the stat entry if no buffs remain
            if not self.temporary_buffs[stat_name]:
                del self.temporary_buffs[stat_name]
                
    def get_stat(self, stat_name):
        """Get a stat's current value including item modifiers and temporary buffs"""
        base_value = self.stats.get(stat_name, 0)
        permanent_multiplier = self.stat_multipliers.get(stat_name, 1.0)
        
        # Apply temporary buffs
        temp_multiplier = 1.0
        if stat_name in self.temporary_buffs:
            for mult, _ in self.temporary_buffs[stat_name]:
                temp_multiplier *= mult
                
        return base_value * permanent_multiplier * temp_multiplier 