import pygame
import random

class CharacterGenerator:
    def __init__(self, size=32):
        self.size = size
        self.colors = {
            'skin': [(200, 170, 150), (180, 150, 130), (160, 130, 110), (140, 110, 90)],
            'hair': [(40, 20, 10), (60, 30, 20), (20, 10, 5), (80, 40, 30)],
            'armor': [(60, 60, 70), (70, 70, 80), (80, 80, 90)],
            'cloth': [(70, 30, 30), (30, 50, 70), (40, 70, 40), (70, 60, 30)],
            'metal': [(90, 90, 100), (100, 100, 110), (110, 110, 120)]
        }

    def generate_character(self):
        """Generate a complete character sprite"""
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Generate each part in order (back to front)
        self._generate_base_body(surface)
        self._generate_armor(surface)
        self._generate_head(surface)
        self._generate_weapon(surface)
        
        return surface
        
    def _generate_base_body(self, surface):
        """Generate the basic body shape"""
        skin_color = random.choice(self.colors['skin'])
        
        # Torso
        torso_height = self.size // 2
        torso_width = self.size // 3
        torso_x = (self.size - torso_width) // 2
        torso_y = self.size // 4
        
        pygame.draw.rect(surface, skin_color, 
                        (torso_x, torso_y, torso_width, torso_height))
                        
        # Add pixel noise for texture
        self._add_noise(surface, torso_x, torso_y, torso_width, torso_height, skin_color)
        
    def _generate_armor(self, surface):
        """Generate armor pieces"""
        armor_color = random.choice(self.colors['armor'])
        metal_color = random.choice(self.colors['metal'])
        
        # Shoulder pads
        shoulder_size = self.size // 8
        for x in [self.size//3 - shoulder_size, 2*self.size//3]:
            pygame.draw.rect(surface, armor_color,
                           (x, self.size//3, shoulder_size, shoulder_size))
            # Add highlights
            pygame.draw.line(surface, metal_color,
                           (x, self.size//3),
                           (x + shoulder_size-1, self.size//3))
                           
        # Chest piece
        chest_width = self.size // 2
        chest_height = self.size // 3
        chest_x = (self.size - chest_width) // 2
        chest_y = self.size // 3
        
        pygame.draw.rect(surface, armor_color,
                        (chest_x, chest_y, chest_width, chest_height))
        # Add armor details
        self._add_armor_details(surface, chest_x, chest_y, chest_width, chest_height, metal_color)
        
    def _generate_head(self, surface):
        """Generate head with hair"""
        skin_color = random.choice(self.colors['skin'])
        hair_color = random.choice(self.colors['hair'])
        
        # Head shape
        head_size = self.size // 4
        head_x = (self.size - head_size) // 2
        head_y = self.size // 8
        
        pygame.draw.rect(surface, skin_color,
                        (head_x, head_y, head_size, head_size))
                        
        # Hair
        hair_style = random.randint(0, 2)
        if hair_style == 0:  # Short hair
            pygame.draw.rect(surface, hair_color,
                           (head_x-1, head_y-1, head_size+2, head_size//2))
        elif hair_style == 1:  # Long hair
            pygame.draw.rect(surface, hair_color,
                           (head_x-1, head_y-1, head_size+2, head_size+4))
        else:  # Spiked hair
            for i in range(3):
                spike_x = head_x + (i * head_size//2)
                spike_height = random.randint(2, 4)
                pygame.draw.line(surface, hair_color,
                               (spike_x, head_y),
                               (spike_x, head_y-spike_height))
                               
    def _generate_weapon(self, surface):
        """Generate a weapon"""
        metal_color = random.choice(self.colors['metal'])
        
        # Sword
        weapon_x = 3 * self.size // 4
        weapon_y = self.size // 3
        
        # Blade
        pygame.draw.line(surface, metal_color,
                        (weapon_x, weapon_y),
                        (weapon_x + self.size//8, weapon_y + self.size//3), 2)
        # Handle
        pygame.draw.line(surface, (60, 40, 20),
                        (weapon_x, weapon_y),
                        (weapon_x - self.size//16, weapon_y - self.size//16))
        # Guard
        pygame.draw.line(surface, metal_color,
                        (weapon_x - 2, weapon_y),
                        (weapon_x + 2, weapon_y), 2)
                        
    def _add_noise(self, surface, x, y, width, height, base_color):
        """Add noise to a region for texture"""
        for dx in range(width):
            for dy in range(height):
                if random.random() < 0.2:  # 20% chance for noise
                    color_var = random.randint(-10, 10)
                    noise_color = tuple(max(0, min(255, c + color_var)) for c in base_color)
                    surface.set_at((x + dx, y + dy), noise_color)
                    
    def _add_armor_details(self, surface, x, y, width, height, detail_color):
        """Add details to armor pieces"""
        # Add edge highlights
        pygame.draw.line(surface, detail_color, (x, y), (x + width-1, y))
        
        # Add rivets
        rivet_positions = [(x + width//4, y + height//4),
                          (x + 3*width//4, y + height//4),
                          (x + width//4, y + 3*height//4),
                          (x + 3*width//4, y + 3*height//4)]
                          
        for rx, ry in rivet_positions:
            pygame.draw.circle(surface, detail_color, (rx, ry), 1) 