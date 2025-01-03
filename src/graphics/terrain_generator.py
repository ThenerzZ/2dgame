import pygame
import random
import noise

class TerrainGenerator:
    def __init__(self, tile_size=32):
        self.tile_size = tile_size
        self.colors = {
            'grass': [(20, 30, 15), (25, 35, 20), (30, 40, 25)],  # Dark grass variations
            'stone': [(40, 40, 45), (45, 45, 50), (50, 50, 55)],  # Dark stone variations
            'path': [(35, 30, 25), (40, 35, 30), (45, 40, 35)],   # Dark dirt path
            'detail': [(15, 15, 15), (20, 20, 20)]                # Dark details
        }
        
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
        """Add grass-like details"""
        for _ in range(random.randint(2, 4)):
            x = random.randint(0, self.tile_size-2)
            height = random.randint(2, 4)
            color = random.choice(self.colors['detail'])
            
            # Draw grass blade
            for y in range(height):
                pos_y = self.tile_size - y - 1
                surface.set_at((x, pos_y), color)
                if random.random() < 0.5:  # 50% chance for wider grass
                    surface.set_at((x+1, pos_y), color)
                    
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
        for _ in range(random.randint(4, 6)):
            x = random.randint(0, self.tile_size-1)
            y = random.randint(0, self.tile_size-1)
            color = random.choice(self.colors['detail'])
            
            # Draw small stones
            surface.set_at((x, y), color)
            if random.random() < 0.3:  # 30% chance for larger stones
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < self.tile_size and 0 <= new_y < self.tile_size:
                        surface.set_at((new_x, new_y), color)
                        
    def generate_chunk(self, width, height, seed=None):
        """Generate a chunk of terrain using Perlin noise"""
        if seed:
            random.seed(seed)
            
        chunk_surface = pygame.Surface((width * self.tile_size, height * self.tile_size))
        
        # Generate noise map
        scale = 50.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0
        
        noise_map = []
        for y in range(height):
            row = []
            for x in range(width):
                n = noise.pnoise2(x/scale, 
                                y/scale, 
                                octaves=octaves, 
                                persistence=persistence, 
                                lacunarity=lacunarity, 
                                repeatx=width, 
                                repeaty=height, 
                                base=seed if seed else 0)
                row.append(n)
            noise_map.append(row)
            
        # Convert noise to terrain
        for y in range(height):
            for x in range(width):
                n = noise_map[y][x]
                
                # Determine tile type based on noise value
                if n < -0.2:
                    tile_type = 'stone'
                elif n < 0.1:
                    tile_type = 'path'
                else:
                    tile_type = 'grass'
                    
                tile = self.generate_tile(tile_type)
                chunk_surface.blit(tile, (x * self.tile_size, y * self.tile_size))
                
        return chunk_surface 