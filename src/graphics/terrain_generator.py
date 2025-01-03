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
            'grass': [(20, 30, 15), (25, 35, 20), (30, 40, 25)],  # Dark, moody grass
            'stone': [(45, 45, 50), (40, 40, 45), (35, 35, 40)],  # Dark stone
            'path': [(35, 30, 25), (40, 35, 30), (45, 40, 35)],   # Dark earthen path
            'detail': [(15, 15, 15), (20, 20, 20)],               # Very dark details
            'ruins': [(55, 50, 45), (50, 45, 40), (45, 40, 35)],  # Ancient weathered ruins
            'tree': [(20, 30, 15), (15, 25, 10), (25, 35, 20)],   # Dark forest trees
            'crystal': [(60, 20, 90), (70, 30, 100), (50, 10, 80)],  # Dark purple crystals
            'fire': [(200, 60, 0), (180, 50, 0), (160, 40, 0)],   # Deep orange fire
            'ember': [(255, 30, 0), (200, 20, 0), (150, 10, 0)],  # Dark red embers
            'flower': [(80, 20, 30), (70, 15, 25), (90, 25, 35)], # Dark red flowers
            'mushroom': [(50, 10, 10), (40, 8, 8), (60, 12, 12)], # Blood-red mushrooms
            'water': [(10, 20, 30), (15, 25, 35), (20, 30, 40)],  # Dark murky water
            'fog': [(20, 20, 25, 0), (25, 25, 30, 0), (30, 30, 35, 0)],  # Atmospheric fog
            'snow': [(200, 200, 220), (180, 180, 200), (160, 160, 180)],  # Cold snow
            'ash': [(50, 50, 55), (45, 45, 50), (40, 40, 45)],    # Dark ash
            'blood': [(120, 0, 0), (100, 0, 0), (80, 0, 0)]       # Blood rain
        }
        
        # Weather types and their properties
        self.weather_types = {
            'clear': {
                'fog_density': 0,
                'particle_count': 0,
                'wind_strength': 0.5,
                'ambient_darkness': 0,
                'weight': 15
            },
            'light_rain': {
                'fog_density': 30,
                'particle_count': 100,
                'wind_strength': 1.2,
                'ambient_darkness': 30,
                'weight': 20
            },
            'heavy_rain': {
                'fog_density': 60,
                'particle_count': 200,
                'wind_strength': 2.5,
                'ambient_darkness': 60,
                'weight': 15
            },
            'blood_rain': {
                'fog_density': 45,
                'particle_count': 150,
                'wind_strength': 2.0,
                'ambient_darkness': 70,
                'particle_color': 'blood',
                'weight': 5
            },
            'ash_storm': {
                'fog_density': 80,
                'particle_count': 250,
                'wind_strength': 3.0,
                'ambient_darkness': 80,
                'particle_color': 'ash',
                'weight': 10
            },
            'snow': {
                'fog_density': 40,
                'particle_count': 150,
                'wind_strength': 1.0,
                'ambient_darkness': 20,
                'particle_color': 'snow',
                'weight': 15
            },
            'heavy_fog': {
                'fog_density': 100,
                'particle_count': 0,
                'wind_strength': 0.4,
                'ambient_darkness': 50,
                'weight': 20
            }
        }
        
        self.bonfire_positions = []
        self.bonfire_particles = {}
        
        # Animation settings
        self.animation_timer = 0
        self.grass_offset = 0
        self.ANIMATION_SPEED = 0.1
        
        # Weather state
        self.current_weather = self._get_random_weather()  # Start with random weather
        self.weather_transition = 0
        self.weather_duration = random.randint(FPS * 20, FPS * 40)
        self.weather_timer = 0
        
        # Initialize weather effects
        self.weather_effects = {
            'particles': [],
            'fog_particles': [],
            'puddles': []
        }
        self.fog_offset = 0
        self.wind_direction = random.uniform(-1, 1)
        self.wind_strength = 1.0
        
        # Initialize weather
        self._init_weather_effects()
        
    def _get_random_weather(self):
        """Get a random weather type based on weights"""
        total_weight = sum(weather['weight'] for weather in self.weather_types.values())
        roll = random.uniform(0, total_weight)
        current_weight = 0
        
        for weather_type, properties in self.weather_types.items():
            current_weight += properties['weight']
            if roll <= current_weight:
                return weather_type
        
        return 'clear'  # Fallback

    def _init_weather_effects(self):
        """Initialize weather effects based on current weather type"""
        weather = self.weather_types[self.current_weather]
        
        # Clear existing effects
        self.weather_effects['particles'].clear()
        self.weather_effects['fog_particles'].clear()
        
        # Initialize particles based on weather type
        particle_color = weather.get('particle_color', 'water')
        for _ in range(weather['particle_count']):
            if self.current_weather == 'snow':
                # Larger snowflakes
                self.weather_effects['particles'].append({
                    'x': random.randint(0, SCREEN_WIDTH),
                    'y': random.randint(-50, SCREEN_HEIGHT),
                    'speed': random.uniform(2, 4),
                    'size': random.randint(3, 6),
                    'rotation': random.uniform(0, 360),
                    'rot_speed': random.uniform(-2, 2),
                    'sway': random.uniform(0, 2*math.pi),
                    'sway_speed': random.uniform(0.02, 0.04),
                    'color': random.choice(self.colors[particle_color]),
                    'points': random.randint(6, 8)
                })
            elif self.current_weather == 'ash_storm':
                # More visible ash and embers
                self.weather_effects['particles'].append({
                    'x': random.randint(0, SCREEN_WIDTH),
                    'y': random.randint(-50, SCREEN_HEIGHT),
                    'speed': random.uniform(3, 8),
                    'size': random.randint(2, 4),
                    'color': random.choice(self.colors[particle_color]),
                    'glow': random.random() < 0.3,
                    'glow_strength': random.uniform(0.7, 1.0),
                    'fade_speed': random.uniform(0.005, 0.015)
                })
            elif self.current_weather == 'blood_rain':
                # More dramatic blood rain
                self.weather_effects['particles'].append({
                    'x': random.randint(0, SCREEN_WIDTH),
                    'y': random.randint(-50, SCREEN_HEIGHT),
                    'speed': random.uniform(15, 20),
                    'size': random.randint(3, 5),
                    'color': random.choice(self.colors[particle_color]),
                    'trail': [],
                    'splatter': False,
                    'splatter_time': 0
                })
            else:
                # Enhanced rain particles
                self.weather_effects['particles'].append({
                    'x': random.randint(0, SCREEN_WIDTH),
                    'y': random.randint(-50, SCREEN_HEIGHT),
                    'speed': random.uniform(20, 25),
                    'size': random.randint(2, 4),
                    'color': random.choice(self.colors[particle_color]),
                    'streak_length': random.randint(8, 12),
                    'ripple': False,
                    'ripple_size': 0
                })
            
        # Initialize enhanced fog particles
        for _ in range(weather['fog_density']):
            self.weather_effects['fog_particles'].append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(60, 100),
                'speed': random.uniform(0.3, 0.6),
                'alpha': random.randint(10, 30),
                'pulse': random.uniform(0, 2*math.pi),
                'pulse_speed': random.uniform(0.02, 0.04)
            })
            
        # Update wind properties
        self.wind_strength = weather['wind_strength']
        self.wind_direction = random.uniform(-1, 1)

    def update_weather(self):
        """Update weather effects and handle weather transitions"""
        # Update weather timer and check for weather change
        self.weather_timer += 1
        if self.weather_timer >= self.weather_duration:
            self._change_weather()
            self.weather_timer = 0
            self.weather_duration = random.randint(FPS * 20, FPS * 40)
        
        weather = self.weather_types[self.current_weather]
        
        # Update particles based on weather type
        for particle in self.weather_effects['particles']:
            if self.current_weather == 'snow':
                # Update snowflake movement
                particle['y'] += particle['speed']
                particle['x'] += math.sin(particle['sway']) * 0.5 + self.wind_direction * self.wind_strength
                particle['rotation'] += particle['rot_speed']
                particle['sway'] += particle['sway_speed']
            elif self.current_weather == 'ash_storm':
                # Update ash particle movement
                particle['y'] += particle['speed']
                particle['x'] += self.wind_direction * self.wind_strength * 2
                if particle['glow']:
                    particle['glow_strength'] = max(0, particle['glow_strength'] - particle['fade_speed'])
            elif self.current_weather == 'blood_rain':
                # Update blood rain movement and trails
                old_x, old_y = particle['x'], particle['y']
                particle['y'] += particle['speed']
                particle['x'] += self.wind_direction * self.wind_strength
                particle['trail'].append((old_x, old_y))
                if len(particle['trail']) > 3:
                    particle['trail'].pop(0)
                
                if particle['splatter']:
                    particle['splatter_time'] += 1
            else:
                # Update rain movement
                particle['y'] += particle['speed']
                particle['x'] += self.wind_direction * self.wind_strength
                if particle['ripple']:
                    particle['ripple_size'] += 0.5
            
            # Reset particles that go off screen
            if particle['y'] > SCREEN_HEIGHT:
                particle['y'] = random.randint(-50, -10)
                particle['x'] = random.randint(0, SCREEN_WIDTH)
                if self.current_weather == 'blood_rain':
                    particle['trail'].clear()
                    particle['splatter'] = True
                    particle['splatter_time'] = 0
                elif 'ripple' in particle:
                    particle['ripple'] = True
                    particle['ripple_size'] = 0
            
            # Wrap particles horizontally
            if particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
            elif particle['x'] < 0:
                particle['x'] = SCREEN_WIDTH
                
        # Update fog particles with pulsing effect
        for particle in self.weather_effects['fog_particles']:
            particle['x'] += particle['speed'] * self.wind_direction
            particle['pulse'] += particle['pulse_speed']
            particle['alpha'] = particle['alpha'] * 0.8 + (particle['alpha'] * math.sin(particle['pulse']) * 0.2)
            
            if particle['x'] > SCREEN_WIDTH:
                particle['x'] = -particle['size']
            elif particle['x'] < -particle['size']:
                particle['x'] = SCREEN_WIDTH

    def _change_weather(self):
        """Randomly change the weather based on weights"""
        # Get list of possible weather types excluding current
        possible_weather = list(self.weather_types.keys())
        possible_weather.remove(self.current_weather)
        
        # Calculate total weight of possible weather types
        total_weight = sum(self.weather_types[w]['weight'] for w in possible_weather)
        roll = random.uniform(0, total_weight)
        current_weight = 0
        
        # Select new weather type based on weights
        for weather_type in possible_weather:
            current_weight += self.weather_types[weather_type]['weight']
            if roll <= current_weight:
                self.current_weather = weather_type
                break
        
        # Reinitialize weather effects for new weather
        self._init_weather_effects()

    def draw_weather(self, screen):
        """Draw weather effects based on current weather type"""
        weather = self.weather_types[self.current_weather]
        
        # Draw enhanced fog layer with pulsing effect
        if weather['fog_density'] > 0:
            fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for particle in self.weather_effects['fog_particles']:
                fog_color = (*random.choice(self.colors['fog'])[:3], 
                           int(particle['alpha'] * (weather['fog_density'] / 60)))
                pygame.draw.circle(fog_surface, fog_color,
                                (int(particle['x']), int(particle['y'])),
                                int(particle['size'] * (0.8 + 0.2 * math.sin(particle['pulse']))))
            screen.blit(fog_surface, (0, 0))
        
        # Draw weather particles with enhanced effects
        if weather['particle_count'] > 0:
            particle_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for particle in self.weather_effects['particles']:
                if self.current_weather == 'snow':
                    # Draw more detailed snowflake
                    center = (int(particle['x']), int(particle['y']))
                    points = []
                    for i in range(particle['points']):
                        angle = math.radians(particle['rotation'] + (360 / particle['points']) * i)
                        point_x = center[0] + math.cos(angle) * particle['size']
                        point_y = center[1] + math.sin(angle) * particle['size']
                        points.append((point_x, point_y))
                        
                        # Add more crystalline details
                        for detail_angle in [45, -45, 30, -30]:
                            detail_rad = math.radians(detail_angle)
                            detail_x = center[0] + math.cos(angle + detail_rad) * particle['size'] * 0.7
                            detail_y = center[1] + math.sin(angle + detail_rad) * particle['size'] * 0.7
                            points.append((detail_x, detail_y))
                            
                    if len(points) >= 3:
                        pygame.draw.polygon(particle_surface, particle['color'], points, 2)
                        
                elif self.current_weather == 'ash_storm':
                    # Draw more visible ash particles with stronger glow
                    if particle['glow'] and particle['glow_strength'] > 0:
                        # Enhanced glow
                        glow_size = particle['size'] * 3
                        glow_alpha = int(100 * particle['glow_strength'])
                        glow_color = (*self.colors['ember'][0], glow_alpha)
                        pygame.draw.circle(particle_surface, glow_color,
                                        (int(particle['x']), int(particle['y'])),
                                        glow_size)
                    # Draw ash particle
                    pygame.draw.rect(particle_surface, particle['color'],
                                   (int(particle['x']), int(particle['y']),
                                    particle['size'], particle['size']))
                    
                elif self.current_weather == 'blood_rain':
                    # Draw more dramatic blood rain
                    if len(particle['trail']) >= 2:
                        # Longer, more visible trails
                        points = [(particle['x'], particle['y'])] + particle['trail']
                        pygame.draw.lines(particle_surface, 
                                        (*particle['color'], 150),
                                        False, points, 3)
                    
                    # Larger blood drops
                    pygame.draw.circle(particle_surface, particle['color'],
                                     (int(particle['x']), int(particle['y'])),
                                     particle['size'])
                    
                    # More dramatic splatter
                    if particle['splatter'] and particle['splatter_time'] < 10:
                        for _ in range(5):
                            angle = random.uniform(0, 2*math.pi)
                            dist = random.uniform(3, 8)
                            splat_x = particle['x'] + math.cos(angle) * dist
                            splat_y = particle['y'] + math.sin(angle) * dist
                            pygame.draw.circle(particle_surface, particle['color'],
                                            (int(splat_x), int(splat_y)),
                                            2)
                else:
                    # Draw enhanced rain drops with longer streaks
                    end_x = particle['x'] + self.wind_direction * particle['streak_length']
                    pygame.draw.line(particle_surface, particle['color'],
                                   (particle['x'], particle['y']),
                                   (end_x, particle['y'] + particle['streak_length']), 3)
                    
                    # More visible ripple effect
                    if particle['ripple'] and particle['ripple_size'] < 15:
                        ripple_alpha = int(max(0, 255 - particle['ripple_size'] * 20))
                        pygame.draw.circle(particle_surface, 
                                         (*particle['color'][:3], ripple_alpha),
                                         (int(particle['x']), SCREEN_HEIGHT),
                                         int(particle['ripple_size']), 2)
            
            screen.blit(particle_surface, (0, 0))
        
        # Apply ambient darkness with more dramatic variation
        if weather['ambient_darkness'] > 0:
            darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            base_alpha = weather['ambient_darkness']
            flicker = random.randint(-10, 10)
            darkness.fill((0, 0, 0, max(0, min(255, base_alpha + flicker))))
            screen.blit(darkness, (0, 0))

    def _create_ripple(self, x, y):
        """Create a ripple effect in the nearest puddle"""
        nearest_puddle = None
        min_dist = float('inf')
        
        for puddle in self.weather_effects['puddles']:
            dx = puddle['x'] - x
            dy = puddle['y'] - y
            dist = dx*dx + dy*dy
            if dist < min_dist and puddle['ripple'] == 0:
                min_dist = dist
                nearest_puddle = puddle
                
        if nearest_puddle and min_dist < 2500:  # Only create ripple if rain hits near puddle
            nearest_puddle['ripple'] = 1

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
        """Add dark fantasy grass details"""
        # Add base grass texture with darker shades
        for _ in range(random.randint(6, 9)):  # More grass for denser look
            x = random.randint(0, self.tile_size-2)
            height = random.randint(2, 4)
            color = random.choice(self.colors['grass'])
            
            # Draw grass blade with darker variations
            for y in range(height):
                pos_y = self.tile_size - y - 1
                # Darken color as grass gets taller
                darkness = max(0, color[0] - y)
                dark_color = (darkness, darkness + 10, darkness)
                surface.set_at((x, pos_y), dark_color)
                if random.random() < 0.7:  # 70% chance for wider grass
                    surface.set_at((x+1, pos_y), dark_color)
        
        # Add sinister flowers occasionally
        if random.random() < 0.1:  # 10% chance for dark flowers
            flower_x = random.randint(2, self.tile_size-4)
            flower_y = random.randint(2, self.tile_size-4)
            flower_color = random.choice(self.colors['flower'])
            
            # Draw small, dark flower
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if abs(dx) + abs(dy) <= 1:  # Cross shape
                        surface.set_at((flower_x + dx, flower_y + dy), flower_color)
                        
        # Add mysterious mushrooms occasionally
        if random.random() < 0.15:  # 15% chance for dark mushrooms
            mush_x = random.randint(2, self.tile_size-4)
            mush_y = random.randint(self.tile_size-6, self.tile_size-2)
            mush_color = random.choice(self.colors['mushroom'])
            
            # Draw eerie mushroom
            surface.set_at((mush_x, mush_y), mush_color)  # Cap
            surface.set_at((mush_x, mush_y+1), (20, 20, 20))  # Dark stem
            # Add slight glow effect
            for dx, dy in [(-1,0), (1,0), (0,-1)]:
                try:
                    surface.set_at((mush_x + dx, mush_y + dy), 
                                 tuple(max(0, c - 10) for c in mush_color))
                except IndexError:
                    continue
            
        # Add animated grass blades
        for _ in range(3):
            x = random.randint(2, self.tile_size-3)
            height = random.randint(4, 6)
            color = random.choice(self.colors['grass'])
            surface.set_at((x, self.tile_size - height), (*color, 128))

    def _add_stone_details(self, surface):
        """Add enhanced stone details"""
        # Add base texture
        for _ in range(random.randint(6, 8)):
            x = random.randint(2, self.tile_size-4)
            y = random.randint(2, self.tile_size-4)
            size = random.randint(2, 4)
            color = random.choice(self.colors['stone'])
            
            # Draw varied stone patterns
            pattern_type = random.choice(['crack', 'circle', 'dots'])
            
            if pattern_type == 'crack':
                # Draw crack-like pattern
                for i in range(size):
                    dx = random.randint(-1, 1)
                    surface.set_at((x+i+dx, y), color)
                    surface.set_at((x+i+dx, y+1), color)
            elif pattern_type == 'circle':
                # Draw small circular pattern
                pygame.draw.circle(surface, color, (x, y), size//2)
            else:  # dots
                # Draw scattered dots
                for _ in range(3):
                    dx = random.randint(-size//2, size//2)
                    dy = random.randint(-size//2, size//2)
                    surface.set_at((x+dx, y+dy), color)

    def _add_path_details(self, surface):
        """Add enhanced path details"""
        # Add base texture
        for _ in range(random.randint(6, 8)):
            x = random.randint(2, self.tile_size-4)
            y = random.randint(2, self.tile_size-4)
            size = random.randint(2, 3)
            color = random.choice(self.colors['path'])
            
            # Draw varied dirt/gravel patterns
            pattern_type = random.choice(['gravel', 'crack', 'dots'])
            
            if pattern_type == 'gravel':
                # Draw small gravel cluster
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if random.random() < 0.7:
                            try:
                                surface.set_at((x+dx, y+dy), color)
                            except IndexError:
                                continue
            elif pattern_type == 'crack':
                # Draw small crack
                for i in range(size):
                    dx = random.randint(-1, 1)
                    surface.set_at((x+i+dx, y), color)
            else:  # dots
                # Scattered dots
                for _ in range(3):
                    dx = random.randint(-2, 2)
                    dy = random.randint(-2, 2)
                    try:
                        surface.set_at((x+dx, y+dy), color)
                    except IndexError:
                        continue
                        
        # Add occasional small rocks
        if random.random() < 0.3:  # 30% chance for rocks
            rock_x = random.randint(2, self.tile_size-4)
            rock_y = random.randint(2, self.tile_size-4)
            rock_color = random.choice(self.colors['stone'])
            
            # Draw small rock
            pygame.draw.circle(surface, rock_color, (rock_x, rock_y), 2)

    def _add_tree(self, surface, x, y):
        """Add enhanced tree"""
        trunk_color = (101, 67, 33)  # Rich brown
        leaves_color = random.choice(self.colors['tree'])
        
        # Draw enhanced trunk
        trunk_width = random.randint(3, 4)
        trunk_height = random.randint(8, 12)
        
        # Add trunk texture
        for tx in range(trunk_width):
            for ty in range(trunk_height):
                if random.random() < 0.8:  # 80% chance for each pixel
                    pixel_x = x + self.tile_size//2 - trunk_width//2 + tx
                    pixel_y = y + self.tile_size//2 + ty
                    color_var = random.randint(-10, 10)
                    trunk_pixel = tuple(max(0, min(255, c + color_var)) for c in trunk_color)
                    surface.set_at((pixel_x, pixel_y), trunk_pixel)
        
        # Draw enhanced leaves
        leaf_positions = [
            (0, -2),  # Top
            (-1, -1), (1, -1),  # Middle
            (-2, 0), (0, 0), (2, 0),  # Bottom
        ]
        
        center_x = x + self.tile_size//2
        center_y = y + self.tile_size//2 - trunk_height//2
        
        for offset_x, offset_y in leaf_positions:
            leaf_x = center_x + offset_x * 4
            leaf_y = center_y + offset_y * 4
            leaf_size = random.randint(3, 5)
            
            # Draw textured leaf cluster
            for dx in range(-leaf_size, leaf_size+1):
                for dy in range(-leaf_size, leaf_size+1):
                    if dx*dx + dy*dy <= leaf_size*leaf_size:
                        if random.random() < 0.8:  # 80% chance for each pixel
                            try:
                                color_var = random.randint(-15, 15)
                                leaf_pixel = tuple(max(0, min(255, c + color_var)) for c in leaves_color)
                                surface.set_at((leaf_x + dx, leaf_y + dy), leaf_pixel)
                            except IndexError:
                                continue

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
        
    def _add_crystal(self, surface, x, y):
        """Add mysterious crystal formation"""
        crystal_color = random.choice(self.colors['crystal'])
        glow_color = (crystal_color[0]+10, crystal_color[1]+10, crystal_color[2]+10)
        
        # Subtle dark glow effect
        for radius in range(6, 2, -1):
            alpha = int(60 * (radius/6))  # More subtle glow
            glow_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*glow_color, alpha),
                            (radius, radius), radius)
            surface.blit(glow_surface,
                        (x + self.tile_size//2 - radius,
                         y + self.tile_size//2 - radius))
        
        # Draw main crystal formation
        crystal_points = []
        num_crystals = random.randint(4, 6)
        center_x = x + self.tile_size//2
        center_y = y + self.tile_size//2
        
        # Create jagged crystal cluster
        for i in range(num_crystals):
            angle = (i / num_crystals) * 6.28 + random.uniform(-0.3, 0.3)
            length = random.randint(4, 7)
            dx = math.cos(angle) * length
            dy = math.sin(angle) * length
            crystal_points.append((center_x + dx, center_y + dy))
            
        if len(crystal_points) >= 3:
            # Draw darker crystal body
            pygame.draw.polygon(surface, crystal_color, crystal_points)
            
            # Add dark highlights
            shadow_color = tuple(max(0, c - 20) for c in crystal_color)
            
            # Draw smaller crystals around the main one
            for i in range(2):
                angle = random.uniform(0, 6.28)
                dist = random.randint(3, 5)
                x_offset = math.cos(angle) * dist
                y_offset = math.sin(angle) * dist
                
                small_crystal_points = []
                for j in range(3):
                    small_angle = (j / 3) * 6.28 + random.uniform(-0.2, 0.2)
                    small_length = random.randint(2, 3)
                    small_dx = math.cos(small_angle) * small_length
                    small_dy = math.sin(small_angle) * small_length
                    small_crystal_points.append((center_x + x_offset + small_dx,
                                              center_y + y_offset + small_dy))
                
                if len(small_crystal_points) >= 3:
                    pygame.draw.polygon(surface, shadow_color, small_crystal_points)
            
    def _add_ruins(self, surface, x, y):
        """Add ancient, dark ruins"""
        ruin_color = random.choice(self.colors['ruins'])
        shadow_color = tuple(max(0, c - 15) for c in ruin_color)
        detail_color = (10, 10, 10)  # Very dark details
        
        # Random ruin type with dark fantasy variations
        ruin_type = random.choice(['dark_pillar', 'broken_wall', 'ancient_arch', 'scattered_ruins'])
        
        if ruin_type == 'dark_pillar':
            # Tall, imposing pillar
            height = random.randint(14, 18)
            width = random.randint(4, 6)
            
            # Draw weathered pillar with dark gradient
            for py in range(height):
                darkness = int(py / height * 10)  # Gradually darker towards bottom
                for px in range(width):
                    if random.random() < 0.9:
                        pixel_x = x + self.tile_size//2 - width//2 + px
                        pixel_y = y + self.tile_size - height + py
                        color_var = random.randint(-5, 5) - darkness
                        pixel_color = tuple(max(0, min(255, c + color_var)) for c in ruin_color)
                        surface.set_at((pixel_x, pixel_y), pixel_color)
            
            # Add ominous cracks
            for _ in range(4):
                crack_x = x + self.tile_size//2 + random.randint(-width//2, width//2)
                crack_y = y + self.tile_size - random.randint(5, height-2)
                crack_length = random.randint(4, 6)
                crack_angle = random.uniform(-0.6, 0.6)
                
                # Draw branching cracks
                for i in range(crack_length):
                    dx = int(math.cos(crack_angle) * i)
                    dy = int(math.sin(crack_angle) * i)
                    surface.set_at((crack_x + dx, crack_y + dy), detail_color)
                    if random.random() < 0.4:  # Branch crack
                        branch_length = random.randint(2, 3)
                        branch_angle = crack_angle + random.uniform(-1, 1)
                        for j in range(branch_length):
                            branch_dx = int(math.cos(branch_angle) * j)
                            branch_dy = int(math.sin(branch_angle) * j)
                            surface.set_at((crack_x + dx + branch_dx, 
                                          crack_y + dy + branch_dy), detail_color)
                    
        elif ruin_type == 'broken_wall':
            # Jagged broken wall
            points = [
                (x + 2, y + self.tile_size - 2),  # Base left
                (x + self.tile_size - 2, y + self.tile_size - 2),  # Base right
                (x + self.tile_size - 4, y + self.tile_size - random.randint(12, 16)),  # Top right
                (x + self.tile_size//2 + random.randint(-2, 2), 
                 y + self.tile_size - random.randint(14, 18)),  # Top middle
                (x + 4, y + self.tile_size - random.randint(10, 14))  # Top left
            ]
            
            # Draw textured wall with shadows
            pygame.draw.polygon(surface, ruin_color, points)
            
            # Add dark weathering and moss
            for _ in range(6):
                detail_x = random.randint(points[0][0], points[1][0])
                detail_y = random.randint(points[4][1], points[1][1])
                detail_size = random.randint(1, 3)
                # Dark stains
                pygame.draw.circle(surface, shadow_color, (detail_x, detail_y), detail_size)
                # Occasional moss or darker detail
                if random.random() < 0.3:
                    moss_color = (20, 30, 15)
                    pygame.draw.circle(surface, moss_color, 
                                     (detail_x + random.randint(-1, 1),
                                      detail_y + random.randint(-1, 1)), 1)
                
        elif ruin_type == 'ancient_arch':
            # Imposing ruined arch
            arch_height = random.randint(14, 18)
            arch_width = random.randint(12, 16)
            center_x = x + self.tile_size//2
            base_y = y + self.tile_size - 2
            
            # Draw weathered pillars
            for side in [-1, 1]:
                pillar_x = center_x + side * arch_width//2
                # Add gradient to pillars
                for py in range(arch_height):
                    darkness = int(py / arch_height * 15)
                    for px in range(3):
                        if random.random() < 0.9:
                            pixel_x = pillar_x + px - 1
                            pixel_y = base_y - py
                            color_var = random.randint(-5, 5) - darkness
                            pixel_color = tuple(max(0, min(255, c + color_var)) for c in ruin_color)
                            surface.set_at((pixel_x, pixel_y), pixel_color)
            
            # Draw broken arch top with gaps
            num_segments = 6
            for i in range(num_segments):
                if random.random() < 0.6:  # 60% chance for each segment
                    angle = (i / (num_segments-1)) * math.pi
                    x_offset = int(math.cos(angle) * arch_width//2)
                    y_offset = int(-math.sin(angle) * arch_height//2)
                    # Draw arch segment with depth
                    for depth in range(2):
                        pygame.draw.circle(surface, shadow_color if depth == 0 else ruin_color,
                                        (center_x + x_offset,
                                         base_y - arch_height + y_offset + depth), 2)
                    
        else:  # scattered_ruins
            # More varied scattered ruins
            for _ in range(random.randint(5, 7)):
                stone_size = random.randint(3, 5)
                stone_x = x + random.randint(4, self.tile_size-4)
                stone_y = y + random.randint(4, self.tile_size-4)
                
                # Draw textured ruins with shadows
                for sx in range(-stone_size, stone_size+1):
                    for sy in range(-stone_size, stone_size+1):
                        if sx*sx + sy*sy <= stone_size*stone_size:
                            if random.random() < 0.8:
                                try:
                                    # Darker towards the bottom
                                    darkness = int((sy + stone_size) / (stone_size * 2) * 15)
                                    color_var = random.randint(-5, 5) - darkness
                                    stone_pixel = tuple(max(0, min(255, c + color_var)) 
                                                      for c in ruin_color)
                                    surface.set_at((stone_x + sx, stone_y + sy), stone_pixel)
                                except IndexError:
                                    continue
                                    
                # Add occasional dark details
                if random.random() < 0.4:
                    detail_x = stone_x + random.randint(-1, 1)
                    detail_y = stone_y + random.randint(-1, 1)
                    surface.set_at((detail_x, detail_y), detail_color)

    def _add_bonfire(self, surface, x, y):
        """Add a mystical bonfire"""
        # Base structure
        center_x = x + self.tile_size // 2
        center_y = y + self.tile_size // 2
        stone_color = random.choice(self.colors['stone'])
        
        # Draw dark stone circle
        for i in range(7):
            angle = (i / 7) * 6.28
            stone_x = center_x + math.cos(angle) * 6
            stone_y = center_y + math.sin(angle) * 6
            # Draw each stone with slight variation
            stone_size = random.randint(2, 3)
            pygame.draw.circle(surface, stone_color, (int(stone_x), int(stone_y)), stone_size)
            # Add darker edge
            pygame.draw.circle(surface, (20, 20, 20), (int(stone_x), int(stone_y)), stone_size, 1)
        
        # Draw charred logs
        log_color = (20, 15, 10)  # Very dark brown
        ember_color = random.choice(self.colors['ember'])
        for i in range(3):
            angle = (i / 3) * 3.14
            log_x = center_x + math.cos(angle) * 3
            log_y = center_y + math.sin(angle) * 3
            # Draw log with ember effect
            pygame.draw.line(surface, log_color,
                           (log_x - 2, log_y),
                           (log_x + 2, log_y), 2)
            # Add glowing ember points
            if random.random() < 0.7:
                surface.set_at((int(log_x), int(log_y)), ember_color)
        
        # Create particle system for this bonfire
        pos = (center_x, center_y)
        self.bonfire_particles[pos] = BonfireParticleSystem(center_x, center_y - 2)
        
        # Add darker, more subtle glow effect
        for radius in range(12, 4, -2):
            alpha = int(20 * (radius/12))  # More subtle glow
            glow_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            glow_color = random.choice(self.colors['fire'])
            pygame.draw.circle(glow_surface, (*glow_color, alpha),
                             (radius, radius), radius)
            surface.blit(glow_surface, 
                        (x + self.tile_size//2 - radius,
                         y + self.tile_size//2 - radius))
        
        return pos
        
    def update_particles(self):
        """Update all particle systems"""
        for particle_system in self.bonfire_particles.values():
            particle_system.update()
            
    def draw_particles(self, screen):
        """Draw all particle systems"""
        for particle_system in self.bonfire_particles.values():
            particle_system.draw(screen) 