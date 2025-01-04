import pygame
import random
import math
from game.settings import *
from graphics.monster_generator import MonsterGenerator
from game.monster_config import MonsterType, get_monster_config, get_death_config, DifficultyTier

class Enemy:
    def __init__(self):
        # Monster type and stats
        self.rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        self.spawn_at_edge()
        
        # Generate sprite
        self.monster_gen = MonsterGenerator(size=32)
        self.sprite = None  # Will be set when type is assigned
        self.death_frames = None  # Will be set when type is assigned
        self.facing_left = False
        
        # Monster type and configuration
        self.monster_type = None
        self.config = None
        
        # Stats will be set from config
        self.health = 0
        self.max_health = 0
        self.damage = 0
        self.speed = 0
        self.kill_reward = 0
        self.tier = None
        
        # Special effects
        self.alpha = 255
        self.has_special_movement = False
        self.special_timer = 0
        
        self.is_dead = False
        self.direction = pygame.math.Vector2()
        
        # Death animation state
        self.death_animation_frame = 0
        self.death_animation_timer = 0
        self.death_animation_duration = 15
        self.frame_duration = 15
        self.corpse_alpha = 255
        self.fade_start = 180
        self.fade_duration = 60
        self.death_particles = []
        
    def set_monster_type(self, monster_type):
        """Set monster type and its associated properties"""
        self.monster_type = monster_type
        self.config = get_monster_config(self.monster_type)
        
        # Convert string tier to DifficultyTier enum
        tier_str = self.config["tier"]
        self.tier = DifficultyTier[tier_str]
        
        # Set stats from config
        stats = self.config["base_stats"]
        self.health = stats["health"]
        self.max_health = stats["health"]
        self.damage = stats["damage"]
        self.speed = stats["speed"]
        
        # Generate sprite and death frames
        type_index = list(MonsterType).index(self.monster_type)
        self.sprite, self.death_frames = self.monster_gen.generate_monster(type_index)
        
        # Set special movement based on monster type
        self.has_special_movement = self.monster_type in [
            MonsterType.SLIME,  # Bouncing movement
            MonsterType.BAT,    # Flying movement
            MonsterType.GHOST,  # Phasing movement
            MonsterType.DEMON,  # Teleporting
            MonsterType.WITCH,  # Floating
            MonsterType.DRAGON  # Flying
        ]
        
    def draw(self, screen):
        if self.is_dead:
            # Draw death animation frame if we have frames and haven't finished animation
            if (self.death_frames and 
                self.death_animation_frame < len(self.death_frames)):
                current_frame = self.death_frames[self.death_animation_frame]
                if current_frame:  # Make sure we have a valid frame
                    current_frame = current_frame.copy()  # Create a copy to modify alpha
                    
                    # Apply fade out effect
                    if self.death_animation_timer > self.fade_start:
                        fade_progress = (self.death_animation_timer - self.fade_start) / self.fade_duration
                        current_frame.set_alpha(max(0, int(255 * (1 - fade_progress))))
                    
                    # Draw the current death frame
                    screen.blit(current_frame, self.rect)
            
            # Draw death particles
            for particle in self.death_particles:
                if 'web' in particle:  # Spider web particles
                    points = []
                    for i in range(3):
                        angle = math.radians(i * 120 + particle['lifetime'] * 2)
                        px = particle['x'] + math.cos(angle) * particle['size']
                        py = particle['y'] + math.sin(angle) * particle['size']
                        points.append((px, py))
                    pygame.draw.lines(screen, (200, 200, 200, particle['alpha']), True, points, 1)
                
                elif 'rotation' in particle:  # Skeleton bone particles
                    bone_surf = pygame.Surface((particle['size'] * 2, particle['size']), pygame.SRCALPHA)
                    pygame.draw.ellipse(bone_surf, (200, 190, 180, particle['alpha']), 
                                     bone_surf.get_rect())
                    rotated = pygame.transform.rotate(bone_surf, particle['rotation'])
                    screen.blit(rotated, (particle['x'] - rotated.get_width()//2,
                                        particle['y'] - rotated.get_height()//2))
                
                elif 'color' in particle:  # Demon fire particles
                    particle_surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), 
                                                pygame.SRCALPHA)
                    color_with_alpha = (*particle['color'], particle['alpha'])
                    pygame.draw.circle(particle_surf, color_with_alpha,
                                    (particle['size'], particle['size']), particle['size'])
                    screen.blit(particle_surf, (particle['x'] - particle['size'],
                                             particle['y'] - particle['size']))
                
                else:  # Default circular particles for slime and ghost
                    particle_surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), 
                                                pygame.SRCALPHA)
                    if 'pulse' in particle:  # Ghost particles
                        color = (200, 200, 255, particle['alpha'])
                    else:  # Slime particles
                        color = (100, 200, 100, particle['alpha'])
                    pygame.draw.circle(particle_surf, color,
                                    (particle['size'], particle['size']), particle['size'])
                    screen.blit(particle_surf, (particle['x'] - particle['size'],
                                             particle['y'] - particle['size']))
            
            # Draw fading corpse
            if self.corpse_alpha > 0:
                corpse_sprite = self.sprite.copy()
                corpse_sprite.set_alpha(self.corpse_alpha)
                if self.tier == DifficultyTier.BASIC:  # Slime flattens
                    scale_y = max(0.2, 1 - (self.death_animation_timer / 20))
                    scaled = pygame.transform.scale(corpse_sprite, 
                                                 (corpse_sprite.get_width(),
                                                  int(corpse_sprite.get_height() * scale_y)))
                    screen.blit(scaled, (self.rect.x, 
                                       self.rect.y + self.rect.height * (1 - scale_y)))
                elif self.tier == DifficultyTier.BOSS:  # Ghost dissipates
                    wave = math.sin(self.death_animation_timer * 0.1) * 5
                    screen.blit(corpse_sprite, (self.rect.x + wave, self.rect.y))
                else:  # Other enemies
                    screen.blit(corpse_sprite, self.rect)
        else:
            # Draw sprite with special effects
            if self.sprite:
                sprite = pygame.transform.flip(self.sprite, self.facing_left, False)
                if self.tier == DifficultyTier.BOSS:  # Ghost-like effect for bosses
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
            indicator_color = ENEMY_TIERS[self.tier.name]["color"]
            pygame.draw.circle(screen, indicator_color, indicator_pos, indicator_radius)
        
    def draw_health_bar(self, screen):
        bar_width = 30
        bar_height = 4
        bar_pos = (self.rect.centerx - bar_width/2, self.rect.top - 6)
        
        # Background (red)
        pygame.draw.rect(screen, RED, (*bar_pos, bar_width, bar_height))
        # Health (color based on tier)
        health_width = (self.health / self.max_health) * bar_width
        tier_color = ENEMY_TIERS[self.tier.name]["color"]
        pygame.draw.rect(screen, tier_color, (*bar_pos, health_width, bar_height))
        
    def update(self, player_pos):
        if self.is_dead:
            # Update death animation
            self.death_animation_timer += 1
            
            # Calculate current animation frame
            if self.death_frames:  # Make sure we have death frames
                frame_index = (self.death_animation_timer // self.frame_duration)
                if frame_index < len(self.death_frames):
                    self.death_animation_frame = frame_index
            
            # Update particles
            for particle in self.death_particles[:]:
                particle['x'] += particle['dx']
                particle['y'] += particle['dy']
                particle['lifetime'] -= 1
                
                if 'rot_speed' in particle:  # For skeleton bones
                    particle['rotation'] += particle['rot_speed']
                    particle['dy'] += 0.2  # Gravity
                
                if 'web' in particle:  # For spider webs
                    particle['alpha'] = max(0, particle['alpha'] - 3)
                
                if 'pulse' in particle:  # For ghost particles
                    particle['alpha'] = 150 + int(50 * math.sin(particle['pulse']))
                    particle['pulse'] += 0.1
                
                if particle['lifetime'] <= 0:
                    self.death_particles.remove(particle)
                    
            # Handle corpse fade
            if self.death_animation_timer > self.fade_start:
                fade_progress = (self.death_animation_timer - self.fade_start) / self.fade_duration
                self.corpse_alpha = max(0, int(255 * (1 - fade_progress)))
                
        else:
            # Update special effects
            if self.has_special_movement:
                self.special_timer += 1
                if self.tier == DifficultyTier.BASIC:  # Slime bounce
                    if self.special_timer % 30 == 0:  # Every half second
                        self.speed = ENEMY_TIERS[self.tier.name]["speed"] * (1.5 if self.speed == ENEMY_TIERS[self.tier.name]["speed"] else 1)
                elif self.tier == DifficultyTier.ELITE:  # Demon teleport
                    if self.special_timer % 180 == 0:  # Every 3 seconds
                        self._teleport_towards(player_pos)
                        return
                elif self.tier == DifficultyTier.BOSS:  # Ghost phase
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
        if self.health <= 0 and not self.is_dead:
            self.is_dead = True
            self.death_animation_frame = 0
            self.death_animation_timer = 0
            self._init_death_particles()
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
        
    def _init_death_particles(self):
        """Initialize death effect particles based on monster type"""
        if not self.monster_type:
            return
            
        particle_config = get_death_config(self.monster_type)["particle_config"]
        
        for _ in range(particle_config["count"]):
            angle = random.uniform(0, 360)
            speed = random.uniform(*particle_config["speed"])
            size = random.uniform(*particle_config["size"])
            lifetime = random.randint(*particle_config["lifetime"])
            
            particle = {
                'x': self.rect.centerx,
                'y': self.rect.centery,
                'dx': math.cos(math.radians(angle)) * speed,
                'dy': math.sin(math.radians(angle)) * speed,
                'size': size,
                'alpha': 255,
                'lifetime': lifetime
            }
            
            # Add type-specific particle properties
            if particle_config["type"] == "bone":
                particle.update({
                    'rotation': random.uniform(0, 360),
                    'rot_speed': random.uniform(-10, 10)
                })
                particle['dy'] -= 2  # Initial upward velocity
            elif particle_config["type"] == "web":
                particle['web'] = True
            elif particle_config["type"] == "fire":
                particle['color'] = random.choice(particle_config["colors"])
            elif particle_config["type"] == "ethereal":
                particle['pulse'] = random.uniform(0, math.pi)
                particle['alpha'] = 200
            
            self.death_particles.append(particle) 