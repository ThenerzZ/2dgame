import pygame
import random
import math
from noise import pnoise2
from game.settings import *
from graphics.particles import BonfireParticleSystem

class TerrainGenerator:
    def __init__(self, tile_size=32):
        self.tile_size = tile_size
        self.colors = {
            'grass': [(20, 30, 15), (25, 35, 20), (30, 40, 25)],  # Dark grass variations
            'stone': [(40, 40, 45), (45, 45, 50), (50, 50, 55)],  # Dark stone variations
            'path': [(35, 30, 25), (40, 35, 30), (45, 40, 35)],   # Dark dirt path
            'detail': [(15, 15, 15), (20, 20, 20)],               # Dark details
            'ruins': [(55, 50, 45), (50, 45, 40), (45, 40, 35)],  # Ancient ruins
            'tree': [(25, 35, 20), (20, 30, 15), (30, 40, 25)],   # Tree colors
            'crystal': [(60, 100, 120), (70, 110, 130), (80, 120, 140)],  # Magic crystals
            'fire': [(255, 100, 0), (255, 160, 0), (255, 130, 0)],  # Fire colors
            'ember': [(255, 50, 0), (255, 80, 0), (200, 40, 0)]     # Ember colors
        }
        self.bonfire_positions = []  # Store bonfire positions for game logic
        self.bonfire_particles = {}  # Store particle systems for each bonfire
        
        # Animation settings
        self.animation_timer = 0
        self.grass_offset = 0
        self.ANIMATION_SPEED = 0.1  # Lower = slower
        
    def generate_tile(self, type='grass'):
        """Generate a single tile with pixel-perfect details"""
        surface = pygame.Surface((self.tile_size, self.tile_size))
        base_color = random.choice(self.colors[type])
        
        # Fill base color
        surface.fill(base_color)
        
        # Add noise pattern
        for x in range(self.tile_size):
            for y in range(self.tile_size):
                if random.random() < 0.2:  # 20% chance for detail pixels
                    # Slightly vary the color
                    color_var = random.randint(-5, 5)
                    pixel_color = tuple(max(0, min(255, c + color_var)) for c in base_color)
                    surface.set_at((x, y), pixel_color)
                    
        # Add details based on type
        if type == 'grass':
            self._add_grass_details(surface)
        elif type == 'stone':
            self._add_stone_details(surface)
        elif type == 'path':
            self._add_path_details(surface)
            
        return surface
        
    def _add_grass_details(self, surface):
        """Add grass-like details with subtle animation support"""
        # Add static grass details
        for _ in range(random.randint(3, 5)):
            x = random.randint(0, self.tile_size-2)
            height = random.randint(2, 4)
            color = random.choice(self.colors['detail'])
            
            # Draw grass blade
            for y in range(height):
                pos_y = self.tile_size - y - 1
                surface.set_at((x, pos_y), color)
                if random.random() < 0.5:  # 50% chance for wider grass
                    surface.set_at((x+1, pos_y), color)
        
        # Add a few taller grass blades that can be animated
        for _ in range(2):
            x = random.randint(2, self.tile_size-3)
            height = random.randint(4, 6)
            color = random.choice(self.colors['grass'])
            
            # Store position for animation
            surface.set_at((x, self.tile_size - height), (*color, 128))  # Semi-transparent marker
                    
    def _add_stone_details(self, surface):
        """Add stone-like details"""
        for _ in range(random.randint(3, 5)):
            x = random.randint(2, self.tile_size-3)
            y = random.randint(2, self.tile_size-3)
            size = random.randint(2, 3)
            color = random.choice(self.colors['detail'])
            
            # Draw crack-like pattern
            for i in range(size):
                surface.set_at((x+i, y), color)
                surface.set_at((x+i, y+1), color)
                
    def _add_path_details(self, surface):
        """Add path-like details"""
        # Add some scattered dirt/gravel details
        for _ in range(random.randint(4, 6)):
            x = random.randint(2, self.tile_size-3)
            y = random.randint(2, self.tile_size-3)
            size = random.randint(1, 2)
            color = random.choice(self.colors['detail'])
            
            # Draw small gravel/dirt patches
            for dx in range(size):
                for dy in range(size):
                    if random.random() < 0.7:  # 70% chance to draw each pixel
                        surface.set_at((x + dx, y + dy), color)
                        
        # Add some path edge variation
        for _ in range(2):
            x = random.randint(0, self.tile_size-1)
            height = random.randint(2, 3)
            color = random.choice(self.colors['path'])
            
            # Draw edge detail
            for y in range(height):
                if random.random() < 0.8:  # 80% chance to draw each pixel
                    surface.set_at((x, y), color)
        
    def update_animations(self):
        """Update subtle grass animations"""
        self.animation_timer += self.ANIMATION_SPEED
        self.grass_offset = math.sin(self.animation_timer) * 1.5  # Subtle movement
        
    def draw_animated_details(self, screen, pos, tile_type):
        """Draw animated details over the base terrain"""
        if tile_type == 'grass':
            # Draw animated grass blades
            x, y = pos
            offset = int(self.grass_offset)
            color = random.choice(self.colors['grass'])
            
            # Draw a few subtle swaying grass blades
            for i in range(2):
                blade_x = x + random.randint(2, self.tile_size-3)
                height = random.randint(4, 6)
                top_x = blade_x + offset
                
                if 0 <= top_x < SCREEN_WIDTH:  # Ensure we don't draw outside screen
                    pygame.draw.line(screen, color, 
                                   (blade_x, y + self.tile_size - height),
                                   (top_x, y + self.tile_size - height - 2), 1) 
        
    def generate_chunk(self, width, height, seed=None):
        """Generate a chunk of terrain using Perlin noise"""
        if seed:
            random.seed(seed)
            
        chunk_surface = pygame.Surface((width * self.tile_size, height * self.tile_size))
        self.bonfire_positions.clear()
        
        # Generate multiple noise maps for different features
        scale = 50.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0
        
        # Multiple noise layers for better terrain variety
        terrain_noise = self._generate_noise_map(width, height, scale, octaves, persistence, lacunarity, seed)
        feature_noise = self._generate_noise_map(width, height, scale/2, 4, 0.6, 2.0, seed+1 if seed else None)
        detail_noise = self._generate_noise_map(width, height, scale/4, 2, 0.3, 2.0, seed+2 if seed else None)
        
        # Pre-calculate bonfire positions to ensure minimum spacing
        min_bonfire_distance = 150  # Minimum pixels between bonfires
        desired_bonfires = 5  # Aim for this many bonfires
        attempts = 0
        max_attempts = 100
        
        while len(self.bonfire_positions) < desired_bonfires and attempts < max_attempts:
            x = random.randint(50, width * self.tile_size - 50)
            y = random.randint(50, height * self.tile_size - 50)
            
            # Check distance from other bonfires
            too_close = False
            for pos in self.bonfire_positions:
                dx = pos[0] - x
                dy = pos[1] - y
                if (dx * dx + dy * dy) < min_bonfire_distance * min_bonfire_distance:
                    too_close = True
                    break
            
            if not too_close:
                self.bonfire_positions.append((x, y))
            
            attempts += 1
        
        # Generate base terrain
        for y in range(height):
            for x in range(width):
                n = terrain_noise[y][x]
                f = feature_noise[y][x]
                d = detail_noise[y][x]
                
                # Enhanced terrain type determination
                if n < -0.3:
                    tile_type = 'stone'
                elif n < -0.1:
                    tile_type = 'path' if d > 0 else 'stone'
                else:
                    if d < -0.2:
                        tile_type = 'path'
                    else:
                        tile_type = 'grass'
                    
                tile = self.generate_tile(tile_type)
                chunk_surface.blit(tile, (x * self.tile_size, y * self.tile_size))
                
                # Add features based on combined noise values
                if f > 0.3 and random.random() < 0.3:
                    if tile_type == 'grass':
                        if d > 0.2:  # Use detail noise for feature distribution
                            self._add_tree(chunk_surface, x * self.tile_size, y * self.tile_size)
                        elif d < -0.2:
                            self._add_crystal(chunk_surface, x * self.tile_size, y * self.tile_size)
                    elif tile_type == 'stone' and random.random() < 0.4:
                        self._add_ruins(chunk_surface, x * self.tile_size, y * self.tile_size)
        
        # Add bonfires at pre-calculated positions
        for pos in self.bonfire_positions:
            self._add_bonfire(chunk_surface, pos[0] - self.tile_size//2, pos[1] - self.tile_size//2)
        
        return chunk_surface
        
    def _generate_noise_map(self, width, height, scale, octaves, persistence, lacunarity, seed=None):
        """Generate a noise map with given parameters"""
        noise_map = []
        for y in range(height):
            row = []
            for x in range(width):
                n = pnoise2(x/scale, 
                          y/scale, 
                          octaves=octaves, 
                          persistence=persistence, 
                          lacunarity=lacunarity, 
                          repeatx=width, 
                          repeaty=height, 
                          base=seed if seed else 0)
                row.append(n)
            noise_map.append(row)
        return noise_map
        
    def _add_tree(self, surface, x, y):
        """Add a tree to the terrain"""
        trunk_color = (40, 25, 15)
        leaves_color = random.choice(self.colors['tree'])
        
        # Draw trunk
        trunk_width = random.randint(2, 3)
        trunk_height = random.randint(6, 8)
        pygame.draw.rect(surface, trunk_color,
                        (x + self.tile_size//2 - trunk_width//2,
                         y + self.tile_size//2,
                         trunk_width, trunk_height))
        
        # Draw leaves
        leaf_size = random.randint(8, 12)
        leaf_positions = [
            (x + self.tile_size//2, y + self.tile_size//2 - leaf_size//2),
            (x + self.tile_size//2 - leaf_size//2, y + self.tile_size//2 - leaf_size//4),
            (x + self.tile_size//2 + leaf_size//2, y + self.tile_size//2 - leaf_size//4)
        ]
        
        for pos_x, pos_y in leaf_positions:
            pygame.draw.circle(surface, leaves_color, (pos_x, pos_y), leaf_size//2)
            
    def _add_crystal(self, surface, x, y):
        """Add a magical crystal formation"""
        crystal_color = random.choice(self.colors['crystal'])
        glow_color = (crystal_color[0]+20, crystal_color[1]+20, crystal_color[2]+20)
        
        # Draw base glow
        pygame.draw.circle(surface, (*glow_color, 30),
                         (x + self.tile_size//2, y + self.tile_size//2),
                         random.randint(6, 8))
        
        # Draw crystal formation
        crystal_points = []
        num_crystals = random.randint(3, 5)
        center_x = x + self.tile_size//2
        center_y = y + self.tile_size//2
        
        for i in range(num_crystals):
            angle = (i / num_crystals) * 6.28  # 2π
            length = random.randint(4, 6)
            dx = math.cos(angle) * length
            dy = math.sin(angle) * length
            
            crystal_points.append((center_x + dx, center_y + dy))
            
        if len(crystal_points) >= 3:
            pygame.draw.polygon(surface, crystal_color, crystal_points)
            # Add highlight
            pygame.draw.line(surface, glow_color,
                           crystal_points[0],
                           crystal_points[1], 1)
            
    def _add_ruins(self, surface, x, y):
        """Add ruins to the terrain"""
        ruin_color = random.choice(self.colors['ruins'])
        
        # Random ruin type
        ruin_type = random.randint(0, 2)
        
        if ruin_type == 0:  # Broken pillar
            height = random.randint(10, 15)
            width = random.randint(4, 6)
            pygame.draw.rect(surface, ruin_color,
                           (x + self.tile_size//2 - width//2,
                            y + self.tile_size - height,
                            width, height))
            # Add cracks
            for _ in range(2):
                crack_x = x + self.tile_size//2 + random.randint(-2, 2)
                crack_y = y + self.tile_size - random.randint(5, height-2)
                pygame.draw.line(surface, (0, 0, 0),
                               (crack_x, crack_y),
                               (crack_x + random.randint(-2, 2),
                                crack_y + random.randint(2, 4)))
                
        elif ruin_type == 1:  # Broken wall
            pygame.draw.polygon(surface, ruin_color, [
                (x + 2, y + self.tile_size - 2),
                (x + self.tile_size - 2, y + self.tile_size - 2),
                (x + self.tile_size - 4, y + self.tile_size - random.randint(8, 12)),
                (x + 4, y + self.tile_size - random.randint(6, 10))
            ])
            
        else:  # Scattered stones
            for _ in range(random.randint(3, 5)):
                stone_size = random.randint(2, 4)
                stone_x = x + random.randint(4, self.tile_size-4)
                stone_y = y + random.randint(4, self.tile_size-4)
                pygame.draw.rect(surface, ruin_color,
                               (stone_x, stone_y, stone_size, stone_size))
                               
    def _add_bonfire(self, surface, x, y):
        """Add a bonfire with animated-like flames"""
        # Base structure (stones in a circle)
        center_x = x + self.tile_size // 2
        center_y = y + self.tile_size // 2
        stone_color = random.choice(self.colors['stone'])
        
        # Draw stone circle
        for i in range(6):
            angle = (i / 6) * 6.28
            stone_x = center_x + math.cos(angle) * 6
            stone_y = center_y + math.sin(angle) * 6
            pygame.draw.circle(surface, stone_color, (int(stone_x), int(stone_y)), 2)
        
        # Draw logs
        log_color = (40, 25, 15)
        for i in range(3):
            angle = (i / 3) * 3.14
            log_x = center_x + math.cos(angle) * 3
            log_y = center_y + math.sin(angle) * 3
            pygame.draw.line(surface, log_color,
                           (log_x - 2, log_y),
                           (log_x + 2, log_y), 2)
        
        # Create particle system for this bonfire
        pos = (center_x, center_y)
        self.bonfire_particles[pos] = BonfireParticleSystem(center_x, center_y - 2)
        
        # Add base glow effect
        glow_surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 100, 0, 30),
                         (self.tile_size//2, self.tile_size//2), 12)
        surface.blit(glow_surface, (x, y))
        
        return pos  # Return position for game logic 
        
    def update_particles(self):
        """Update all particle systems"""
        for particle_system in self.bonfire_particles.values():
            particle_system.update()
            
    def draw_particles(self, screen):
        """Draw all particle systems"""
        for particle_system in self.bonfire_particles.values():
            particle_system.draw(screen) 