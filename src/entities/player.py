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
        
        # Weapon positions (4 fixed spots around character)
        self.weapon_positions = [
            {'offset': (25, 0), 'base_angle': 0},    # Right
            {'offset': (0, -25), 'base_angle': 90},  # Top
            {'offset': (-25, 0), 'base_angle': 180}, # Left
            {'offset': (0, 25), 'base_angle': 270}   # Bottom
        ]
        
        # Equipment system
        self.equipment_sprites = EquipmentSprites(PLAYER_SIZE)
        self.weapons = []  # List of equipped weapons (max 4)
        self.weapon_sprites = []  # List of weapon sprites
        self.weapon_animations = []  # List of weapon animations
        self.weapon_cooldowns = []  # Cooldown for each weapon
        self.weapon_particles = []  # Particle effects for each weapon
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
                # Get animation for this weapon
                animation = self.equipment_sprites.get_animation(item.name)
                self.weapon_animations.append(animation)
                self.weapon_cooldowns.append(0)
                # Create particle system for this weapon
                self.weapon_particles.append(BulletParticleSystem())
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
                self.weapon_animations.pop(index)
                self.weapon_cooldowns.pop(index)
                self.weapon_particles.pop(index)
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
        
        # Update weapon cooldowns and animations
        for i in range(len(self.weapon_cooldowns)):
            if self.weapon_cooldowns[i] > 0:
                self.weapon_cooldowns[i] -= 1
            if i < len(self.weapon_animations) and self.weapon_animations[i]:
                self.weapon_animations[i].update()
        
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
            
            # Draw all equipped weapons with animations in their fixed positions
            for i, weapon_sprite in enumerate(self.weapon_sprites):
                if weapon_sprite and i < len(self.weapons):
                    # Get the fixed position for this weapon
                    pos = self.weapon_positions[i]
                    
                    # Calculate weapon position relative to character center
                    weapon_x = self.rect.centerx + pos['offset'][0]
                    weapon_y = self.rect.centery + pos['offset'][1]
                    
                    # Calculate weapon angle based on movement and base position
                    if self.direction.magnitude() > 0:
                        target_angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
                    else:
                        target_angle = pos['base_angle']
                    
                    # Draw weapon animation if it exists
                    if i < len(self.weapon_animations) and self.weapon_animations[i]:
                        self.weapon_animations[i].draw(screen, weapon_x, weapon_y, target_angle)
                    else:
                        # Fallback to static sprite
                        rotated_weapon = pygame.transform.rotate(weapon_sprite, -target_angle)
                        weapon_rect = rotated_weapon.get_rect(center=(weapon_x, weapon_y))
                        screen.blit(rotated_weapon, weapon_rect)
                    
                    # Draw attack effects if attacking and cooldown is active
                    if self.is_attacking and self.weapon_cooldowns[i] > 0:
                        self._draw_attack_effects(screen, weapon_x, weapon_y, self.weapons[i])
                        
                        # Add weapon-specific particles
                        if i < len(self.weapon_particles):
                            self.weapon_particles[i].update()
                            self.weapon_particles[i].draw(screen)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw bullets and effects
        self.bullet_system.draw(screen)
        
        self.draw_health_bar(screen)

    def _draw_attack_effects(self, screen, weapon_x, weapon_y, weapon):
        """Draw weapon-specific attack effects"""
        if weapon is None:  # Basic attack effect
            # Enhanced slash effect with better positioning
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
            # Calculate tip of the wand
            wand_length = 30
            tip_x = weapon_x + math.cos(math.radians(self.weapon_angle)) * wand_length
            tip_y = weapon_y + math.sin(math.radians(self.weapon_angle)) * wand_length
            
            # Draw magic beam
            beam_length = 40
            beam_end_x = tip_x + math.cos(math.radians(self.weapon_angle)) * beam_length
            beam_end_y = tip_y + math.sin(math.radians(self.weapon_angle)) * beam_length
            
            # Draw lightning beam
            segments = 6
            points = [(tip_x, tip_y)]
            for i in range(segments):
                prev_x, prev_y = points[-1]
                progress = (i + 1) / segments
                target_x = tip_x + (beam_end_x - tip_x) * progress
                target_y = tip_y + (beam_end_y - tip_y) * progress
                offset = random.uniform(-5, 5) * (1 - progress)  # Less deviation near the end
                points.append((target_x + offset, target_y + offset))
            
            # Draw main beam
            for i in range(len(points) - 1):
                pygame.draw.line(screen, (100, 200, 255, 200), points[i], points[i + 1], 2)
            
            # Add sparkle effects at the tip
            for _ in range(4):
                spark_angle = self.weapon_angle + random.uniform(-30, 30)
                spark_dist = random.uniform(2, 8)
                spark_x = tip_x + math.cos(math.radians(spark_angle)) * spark_dist
                spark_y = tip_y + math.sin(math.radians(spark_angle)) * spark_dist
                
                # Draw star sparkle
                size = random.uniform(2, 4)
                spark_points = []
                for i in range(5):
                    point_angle = spark_angle + (i * 72)
                    px = spark_x + math.cos(math.radians(point_angle)) * size
                    py = spark_y + math.sin(math.radians(point_angle)) * size
                    spark_points.append((px, py))
                pygame.draw.polygon(screen, (200, 220, 255, 200), spark_points)
        
        elif weapon.name == "Fire Wand":
            # Calculate tip of the wand
            wand_length = 25
            tip_x = weapon_x + math.cos(math.radians(self.weapon_angle)) * wand_length
            tip_y = weapon_y + math.sin(math.radians(self.weapon_angle)) * wand_length
            
            # Enhanced fire trail effect
            for _ in range(8):
                angle = self.weapon_angle + random.uniform(-25, 25)
                distance = random.uniform(5, 35)
                effect_x = tip_x + math.cos(math.radians(angle)) * distance
                effect_y = tip_y + math.sin(math.radians(angle)) * distance
                
                # Flame particles with better layering
                size = random.uniform(4, 8) * (1 - distance/35)  # Smaller particles further out
                alpha = int(255 * (1 - distance/35))
                
                colors = [
                    (255, 255, 200, alpha),  # White-hot core
                    (255, 200, 50, alpha),   # Yellow middle
                    (255, 150, 50, alpha),   # Orange outer
                    (255, 100, 50, alpha),   # Red edge
                ]
                
                for i, color in enumerate(colors):
                    flame_size = size * (1 - i * 0.2)
                    flame_surf = pygame.Surface((int(flame_size * 2), int(flame_size * 2)), pygame.SRCALPHA)
                    pygame.draw.circle(flame_surf, color, 
                                    (int(flame_size), int(flame_size)), int(flame_size))
                    screen.blit(flame_surf, (effect_x - flame_size, effect_y - flame_size))
                    
                # Add ember particles
                if random.random() < 0.3:
                    ember_x = effect_x + random.uniform(-5, 5)
                    ember_y = effect_y + random.uniform(-5, 5)
                    ember_size = random.uniform(1, 2)
                    pygame.draw.circle(screen, (255, 200, 50, alpha), 
                                    (int(ember_x), int(ember_y)), int(ember_size))
        
        elif weapon.name == "Cross Bow":
            # Calculate bow tip position
            bow_length = 20
            tip_x = weapon_x + math.cos(math.radians(self.weapon_angle)) * bow_length
            tip_y = weapon_y + math.sin(math.radians(self.weapon_angle)) * bow_length
            
            # Enhanced arrow effects
            trail_length = 40
            num_arrows = 3
            spread_angles = [-15, 0, 15]  # Fixed spread pattern
            
            for spread in spread_angles:
                trail_angle = self.weapon_angle + spread
                # Draw arrow trail with fading effect
                num_segments = 8
                for i in range(num_segments):
                    progress = i / num_segments
                    start_dist = progress * trail_length
                    end_dist = (progress + 1/num_segments) * trail_length
                    
                    start_x = tip_x + math.cos(math.radians(trail_angle)) * start_dist
                    start_y = tip_y + math.sin(math.radians(trail_angle)) * start_dist
                    end_x = tip_x + math.cos(math.radians(trail_angle)) * end_dist
                    end_y = tip_y + math.sin(math.radians(trail_angle)) * end_dist
                    
                    alpha = int(255 * (1 - progress))
                    pygame.draw.line(screen, (150, 150, 150, alpha), 
                                   (start_x, start_y), (end_x, end_y), 2)
                
                # Draw enhanced arrowhead
                head_x = tip_x + math.cos(math.radians(trail_angle)) * trail_length
                head_y = tip_y + math.sin(math.radians(trail_angle)) * trail_length
                
                head_size = 6
                head_points = [
                    (head_x, head_y),
                    (head_x - head_size * math.cos(math.radians(trail_angle + 140)),
                     head_y - head_size * math.sin(math.radians(trail_angle + 140))),
                    (head_x - head_size * 0.5 * math.cos(math.radians(trail_angle)),
                     head_y - head_size * 0.5 * math.sin(math.radians(trail_angle))),
                    (head_x - head_size * math.cos(math.radians(trail_angle - 140)),
                     head_y - head_size * math.sin(math.radians(trail_angle - 140)))
                ]
                pygame.draw.polygon(screen, (180, 180, 180), head_points)
                
                # Add motion blur particles
                for _ in range(2):
                    particle_x = head_x + random.uniform(-5, 5)
                    particle_y = head_y + random.uniform(-5, 5)
                    particle_size = random.uniform(1, 2)
                    pygame.draw.circle(screen, (150, 150, 150, 100),
                                    (int(particle_x), int(particle_y)), int(particle_size))
        
        elif weapon.name == "Whip":
            # Calculate whip base position
            whip_segments = 10
            segment_length = 8
            points = [(weapon_x, weapon_y)]
            
            # Create dynamic whip curve
            wave_time = pygame.time.get_ticks() / 200.0  # Time-based animation
            for i in range(whip_segments):
                progress = i / whip_segments
                angle = self.weapon_angle + math.sin(wave_time + i * 0.5) * 40 * progress
                prev_x, prev_y = points[-1]
                next_x = prev_x + math.cos(math.radians(angle)) * segment_length
                next_y = prev_y + math.sin(math.radians(angle)) * segment_length
                points.append((next_x, next_y))
                
                # Add dynamic particles along whip
                if random.random() < 0.6:
                    particle_angle = angle + random.uniform(-60, 60)
                    particle_dist = random.uniform(2, 6) * progress
                    particle_x = next_x + math.cos(math.radians(particle_angle)) * particle_dist
                    particle_y = next_y + math.sin(math.radians(particle_angle)) * particle_dist
                    particle_size = random.uniform(1, 2) * (1 - progress)
                    alpha = int(200 * (1 - progress))
                    pygame.draw.circle(screen, (200, 150, 100, alpha), 
                                    (int(particle_x), int(particle_y)), int(particle_size))
            
            # Draw whip segments with dynamic thickness and color gradient
            for i in range(len(points) - 1):
                progress = i / (len(points) - 1)
                width = max(1, 4 - (i // 2))
                color = (
                    139 - int(40 * progress),
                    69 - int(20 * progress),
                    19,
                    255 - int(100 * progress)
                )
                pygame.draw.line(screen, color, points[i], points[i + 1], width)
            
            # Add crack effect at whip tip
            if len(points) > 1:
                tip_x, tip_y = points[-1]
                for _ in range(4):
                    spark_angle = self.weapon_angle + random.uniform(-30, 30)
                    spark_length = random.uniform(3, 8)
                    end_x = tip_x + math.cos(math.radians(spark_angle)) * spark_length
                    end_y = tip_y + math.sin(math.radians(spark_angle)) * spark_length
                    pygame.draw.line(screen, (200, 150, 100, 150),
                                   (tip_x, tip_y), (end_x, end_y), 1)
        
        elif weapon.name == "Lightning Ring":
            # Calculate ring center
            ring_radius = 20
            center_x = weapon_x + math.cos(math.radians(self.weapon_angle)) * ring_radius
            center_y = weapon_y + math.sin(math.radians(self.weapon_angle)) * ring_radius
            
            # Draw the base ring with glow
            ring_surf = pygame.Surface((ring_radius * 4, ring_radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(ring_surf, (100, 150, 255, 30), 
                             (ring_radius * 2, ring_radius * 2), ring_radius * 2)  # Outer glow
            pygame.draw.circle(ring_surf, (100, 150, 255, 60), 
                             (ring_radius * 2, ring_radius * 2), ring_radius * 1.5)  # Middle glow
            pygame.draw.circle(ring_surf, (100, 150, 255, 100), 
                             (ring_radius * 2, ring_radius * 2), ring_radius, 2)  # Main ring
            screen.blit(ring_surf, (center_x - ring_radius * 2, center_y - ring_radius * 2))
            
            # Enhanced lightning bolts
            num_bolts = 4
            for i in range(num_bolts):
                start_angle = self.weapon_angle + (i * 360 / num_bolts) + random.uniform(-10, 10)
                start_x = center_x + math.cos(math.radians(start_angle)) * ring_radius
                start_y = center_y + math.sin(math.radians(start_angle)) * ring_radius
                
                # Create lightning path
                points = [(start_x, start_y)]
                bolt_length = random.uniform(30, 40)
                segments = 5
                
                for j in range(segments):
                    prev_x, prev_y = points[-1]
                    progress = (j + 1) / segments
                    angle = start_angle + random.uniform(-40, 40) * (1 - progress)
                    length = bolt_length / segments
                    next_x = prev_x + math.cos(math.radians(angle)) * length
                    next_y = prev_y + math.sin(math.radians(angle)) * length
                    points.append((next_x, next_y))
                
                # Draw main lightning bolt with glow
                for j in range(len(points) - 1):
                    # Outer glow
                    pygame.draw.line(screen, (100, 150, 255, 50),
                                   points[j], points[j + 1], 4)
                    # Inner bright line
                    pygame.draw.line(screen, (200, 220, 255, 200),
                                   points[j], points[j + 1], 2)
                
                # Add small arcs between segments
                for j in range(len(points) - 1):
                    if random.random() < 0.5:
                        mid_x = (points[j][0] + points[j + 1][0]) / 2
                        mid_y = (points[j][1] + points[j + 1][1]) / 2
                        arc_size = random.uniform(4, 8)
                        arc_angle = random.uniform(0, 360)
                        arc_surf = pygame.Surface((arc_size * 2, arc_size * 2), pygame.SRCALPHA)
                        pygame.draw.arc(arc_surf, (150, 200, 255, 150),
                                      (0, 0, arc_size * 2, arc_size * 2),
                                      math.radians(arc_angle),
                                      math.radians(arc_angle + random.uniform(30, 90)), 2)
                        screen.blit(arc_surf, (mid_x - arc_size, mid_y - arc_size))

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
                # Start weapon animation
                if self.weapon_animations[i]:
                    self.weapon_animations[i].play()
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
 