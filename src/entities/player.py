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
        self.weapons = []  # List of equipped weapons (max 4)
        self.weapon_sprites = []  # List of weapon sprites
        self.current_weapon_index = 0
        self.armor_overlays = []  # List of armor visual effects
        
        # Animation system
        if self.sprite:
            self.animator = AnimationHandler(self.sprite)
        else:
            self.animator = None
        
        # Weapon state
        self.weapon_offset_x = 20
        self.weapon_offset_y = 0
        self.weapon_angle = 0
        self.is_attacking = False
        self.weapon_cooldowns = []  # Cooldown for each weapon
        
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
        
        # Stat multipliers from items (now they stack)
        self.stat_multipliers = {stat: [] for stat in self.stats.keys()}
        
        # Combat state
        self.is_attacking = False
        self.attack_animation_timer = 0
        self.attack_animation_duration = 5
        self.current_enemies = []  # List of current enemies in range
        self.score = 0  # Track player's score

    def equip_item(self, item):
        """Handle equipping an item and updating visuals"""
        if item.item_type == ItemType.ACTIVE:
            if len(self.weapons) < 4:  # Maximum 4 weapons
                self.weapons.append(item)
                self.weapon_sprites.append(self.equipment_sprites.generate_weapon_sprite(item.name))
                self.weapon_cooldowns.append(0)
                # Apply weapon stats
                item.apply_effect(self)
            else:
                print("Cannot equip more than 4 weapons!")
                return False
        elif item.item_type == ItemType.PASSIVE:
            # Generate armor overlay if the item has a visual effect
            overlay = self.equipment_sprites.generate_armor_overlay(item.name)
            if overlay:
                self.armor_overlays.append(overlay)
            # Apply passive item stats (they now stack)
            item.apply_effect(self)
        return True

    def unequip_item(self, item):
        """Handle unequipping an item and removing visuals"""
        if item.item_type == ItemType.ACTIVE:
            if item in self.weapons:
                index = self.weapons.index(item)
                self.weapons.pop(index)
                self.weapon_sprites.pop(index)
                self.weapon_cooldowns.pop(index)
                if self.current_weapon_index >= len(self.weapons):
                    self.current_weapon_index = max(0, len(self.weapons) - 1)
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
        
        # Update weapon cooldowns
        for i in range(len(self.weapon_cooldowns)):
            if self.weapon_cooldowns[i] > 0:
                self.weapon_cooldowns[i] -= 1
        
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
        
        # Calculate weapon angle based on movement or target
        if self.direction.magnitude() > 0:
            self.weapon_angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
        
        # Update bullet system
        self.bullet_system.update()
        
        # Auto-attack with all weapons that are off cooldown
        self.attack()

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
            
            # Draw all equipped weapons
            for i, weapon_sprite in enumerate(self.weapon_sprites):
                if weapon_sprite:
                    # Calculate offset based on weapon index
                    angle_offset = i * (360 / max(1, len(self.weapon_sprites)))
                    weapon_angle = self.weapon_angle + angle_offset
                    
                    # Calculate weapon position
                    weapon_x = self.rect.centerx + math.cos(math.radians(weapon_angle)) * self.weapon_offset_x
                    weapon_y = self.rect.centery + math.sin(math.radians(weapon_angle)) * self.weapon_offset_y
                    
                    # Rotate weapon
                    rotated_weapon = pygame.transform.rotate(weapon_sprite, -weapon_angle)
                    weapon_rect = rotated_weapon.get_rect(center=(weapon_x, weapon_y))
                    
                    # Draw weapon
                    screen.blit(rotated_weapon, weapon_rect)
                    
                    # Draw attack effects if attacking and cooldown is active
                    if self.is_attacking and self.weapon_cooldowns[i] > 0:
                        self._draw_attack_effects(screen, weapon_x, weapon_y, self.weapons[i])
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw bullets and effects
        self.bullet_system.draw(screen)
        
        self.draw_health_bar(screen)

    def _draw_attack_effects(self, screen, weapon_x, weapon_y, weapon):
        """Draw weapon-specific attack effects"""
        if weapon is None:  # Basic attack effect
            # Enhanced slash effect
            angle = self.weapon_angle
            # Main slash arc
            for i in range(3):
                start_angle = angle - 30 + (i * 30)
                end_angle = start_angle + 30
                radius = 20 + (i * 5)
                rect = pygame.Rect(weapon_x - radius, weapon_y - radius, radius * 2, radius * 2)
                pygame.draw.arc(screen, WHITE, rect, math.radians(start_angle), math.radians(end_angle), 2)
            
            # Additional particle effects
            for _ in range(3):
                particle_angle = angle + random.uniform(-20, 20)
                distance = random.uniform(15, 25)
                effect_x = weapon_x + math.cos(math.radians(particle_angle)) * distance
                effect_y = weapon_y + math.sin(math.radians(particle_angle)) * distance
                
                # Draw small triangles as particles
                points = []
                for i in range(3):
                    point_angle = particle_angle + (i * 120)
                    point_x = effect_x + math.cos(math.radians(point_angle)) * 3
                    point_y = effect_y + math.sin(math.radians(point_angle)) * 3
                    points.append((point_x, point_y))
                
                pygame.draw.polygon(screen, (200, 200, 200), points)
                
        elif weapon.name == "Magic Wand":
            # Magic sparkle effect
            for _ in range(3):
                angle = self.weapon_angle + random.uniform(-30, 30)
                distance = random.uniform(15, 25)
                effect_x = weapon_x + math.cos(math.radians(angle)) * distance
                effect_y = weapon_y + math.sin(math.radians(angle)) * distance
                
                pygame.draw.circle(screen, (100, 200, 255, 150), (int(effect_x), int(effect_y)), 2)
        
        elif weapon.name == "Fire Wand":
            # Fire trail effect
            for _ in range(5):
                angle = self.weapon_angle + random.uniform(-20, 20)
                distance = random.uniform(10, 30)
                effect_x = weapon_x + math.cos(math.radians(angle)) * distance
                effect_y = weapon_y + math.sin(math.radians(angle)) * distance
                
                size = random.uniform(2, 4)
                alpha = int(255 * (1 - distance/30))
                pygame.draw.circle(screen, (255, 100, 0, alpha), 
                                 (int(effect_x), int(effect_y)), int(size))
        
        elif weapon.name == "Lightning Ring":
            # Lightning effect
            for _ in range(2):
                start_angle = self.weapon_angle + random.uniform(-30, 30)
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
        """Get a stat's current value including stacked multipliers"""
        base_value = self.stats.get(stat_name, 0)
        
        # Apply all multipliers
        total_multiplier = 1.0
        if stat_name in self.stat_multipliers:
            for mult in self.stat_multipliers[stat_name]:
                total_multiplier *= mult
                
        return base_value * total_multiplier
        
    def modify_stat(self, stat_name, multiplier):
        """Modify a stat's multiplier (used by items) - now they stack"""
        if stat_name in self.stat_multipliers:
            self.stat_multipliers[stat_name].append(multiplier)
            
    def remove_stat_multiplier(self, stat_name, multiplier):
        """Remove a specific stat multiplier"""
        if stat_name in self.stat_multipliers:
            if multiplier in self.stat_multipliers[stat_name]:
                self.stat_multipliers[stat_name].remove(multiplier)
                
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
        """Attack with all weapons and basic attack if no weapons equipped"""
        damage_dealt = 0
        
        # Basic attack if no weapons equipped
        if not self.weapons:
            if not hasattr(self, 'basic_attack_cooldown'):
                self.basic_attack_cooldown = 0
                
            if self.basic_attack_cooldown <= 0:
                self.basic_attack_cooldown = 0.5 * FPS  # Basic attack every 0.5 seconds
                self.is_attacking = True
                # Calculate basic attack damage
                damage = self.calculate_damage() * 1.0  # Base damage multiplier
                damage_dealt += self._attack_nearest_enemy(damage, None)
            else:
                self.basic_attack_cooldown -= 1
        
        # Weapon attacks
        for i, weapon in enumerate(self.weapons):
            if self.weapon_cooldowns[i] <= 0:
                self.weapon_cooldowns[i] = weapon.weapon_stats.get("cooldown", 1.0) * FPS
                self.is_attacking = True
                # Calculate damage
                damage = self.calculate_damage() * weapon.stats.get("damage", 1.0)
                # Find closest enemy and apply damage
                damage_dealt += self._attack_nearest_enemy(damage, weapon)
            else:
                self.weapon_cooldowns[i] -= 1
                
        return damage_dealt

    def _attack_nearest_enemy(self, damage, weapon):
        """Find and attack the nearest enemy with the given weapon"""
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
            # Create hit particles at enemy position
            if weapon is None:  # Basic attack
                # Create slash particles
                for _ in range(5):
                    angle = self.weapon_angle + random.uniform(-30, 30)
                    speed = random.uniform(2, 5)
                    dx = math.cos(math.radians(angle)) * speed
                    dy = math.sin(math.radians(angle)) * speed
                    self.bullet_system.add_particle(
                        closest_enemy.rect.centerx, 
                        closest_enemy.rect.centery,
                        dx, dy,
                        WHITE,
                        random.randint(5, 10),  # Lifetime
                        random.uniform(2, 4)     # Size
                    )
            
            if closest_enemy.take_damage(damage):
                self.score += 1
                self.add_money(ENEMY_KILL_REWARD)
            return damage
        return 0

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
                
    def calculate_damage(self):
        """Calculate damage with critical hits"""
        base_damage = self.get_stat("damage")
        
        # Check for critical hit
        if random.random() < self.get_stat("crit_chance"):
            return base_damage * self.get_stat("crit_damage")
        return base_damage

    def set_current_enemies(self, enemies):
        """Update the list of current enemies"""
        self.current_enemies = enemies
 