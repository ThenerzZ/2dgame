import pygame
import random

class CharacterGenerator:
    def __init__(self, size=32):
        self.size = size
        self.colors = {
            'skin': [(180, 160, 140), (160, 140, 120)],  # Reduced skin tones for covered areas
            'armor': [
                (40, 40, 45),    # Dark steel
                (30, 30, 35),    # Darker steel
                (25, 25, 30),    # Almost black steel
                (35, 25, 20),    # Dark bronze
            ],
            'cloth': [
                (40, 20, 20),    # Dark red
                (20, 20, 30),    # Dark blue
                (30, 20, 35),    # Dark purple
                (25, 15, 10),    # Dark brown
            ],
            'metal': [
                (70, 70, 80),    # Steel
                (60, 50, 40),    # Bronze
                (50, 50, 60),    # Dark silver
            ],
            'trim': [
                (100, 80, 30),   # Gold trim
                (80, 60, 40),    # Bronze trim
                (60, 60, 70),    # Silver trim
            ]
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
        # Only generate minimal body parts as most will be covered by armor
        skin_color = random.choice(self.colors['skin'])
        
        # Neck only
        neck_width = self.size // 6
        neck_height = self.size // 8
        neck_x = (self.size - neck_width) // 2
        neck_y = self.size // 4
        
        pygame.draw.rect(surface, skin_color, 
                        (neck_x, neck_y, neck_width, neck_height))
                        
    def _generate_armor(self, surface):
        """Generate knight armor pieces"""
        armor_color = random.choice(self.colors['armor'])
        metal_color = random.choice(self.colors['metal'])
        trim_color = random.choice(self.colors['trim'])
        cloth_color = random.choice(self.colors['cloth'])
        
        # Chainmail underlayer
        chainmail_y = self.size // 3
        chainmail_height = self.size // 2
        for y in range(chainmail_y, chainmail_y + chainmail_height, 2):
            for x in range(self.size // 3, 2 * self.size // 3, 2):
                pygame.draw.circle(surface, metal_color, (x, y), 1)
        
        # Chest plate
        chest_width = self.size // 2
        chest_height = self.size // 2
        chest_x = (self.size - chest_width) // 2
        chest_y = self.size // 3
        
        pygame.draw.rect(surface, armor_color,
                        (chest_x, chest_y, chest_width, chest_height))
        
        # Shoulder pauldrons
        pauldron_width = self.size // 4
        pauldron_height = self.size // 4
        for x in [chest_x - pauldron_width//2, chest_x + chest_width - pauldron_width//2]:
            # Main pauldron shape
            points = [
                (x, chest_y),
                (x + pauldron_width, chest_y),
                (x + pauldron_width - 2, chest_y + pauldron_height),
                (x + 2, chest_y + pauldron_height),
            ]
            pygame.draw.polygon(surface, armor_color, points)
            # Trim
            pygame.draw.line(surface, trim_color,
                           points[0], points[1], 1)
        
        # Cape/cloak
        if random.random() < 0.7:  # 70% chance for cape
            cape_points = [
                (chest_x - 2, chest_y),
                (chest_x + chest_width + 2, chest_y),
                (chest_x + chest_width + 4, self.size - 4),
                (chest_x - 4, self.size - 4),
            ]
            pygame.draw.polygon(surface, cloth_color, cape_points)
            # Cape trim
            pygame.draw.line(surface, trim_color,
                           cape_points[0], cape_points[1], 1)
        
        # Armor details
        self._add_armor_details(surface, chest_x, chest_y, chest_width, chest_height, trim_color)
        
    def _generate_head(self, surface):
        """Generate knight helmet"""
        armor_color = random.choice(self.colors['armor'])
        trim_color = random.choice(self.colors['trim'])
        
        # Helmet base
        helmet_size = self.size // 4
        helmet_x = (self.size - helmet_size) // 2
        helmet_y = self.size // 8
        
        pygame.draw.rect(surface, armor_color,
                        (helmet_x, helmet_y, helmet_size, helmet_size))
        
        # Visor
        visor_y = helmet_y + helmet_size // 3
        visor_height = helmet_size // 3
        pygame.draw.rect(surface, (20, 20, 25),  # Darker for visor
                        (helmet_x, visor_y, helmet_size, visor_height))
        
        # Helmet details
        if random.random() < 0.7:  # 70% chance for plume
            plume_height = random.randint(4, 6)
            plume_color = random.choice(self.colors['cloth'])
            for i in range(plume_height):
                x = helmet_x + helmet_size // 2
                y = helmet_y - i
                width = max(1, (plume_height - i) // 2)
                pygame.draw.line(surface, plume_color,
                               (x - width, y), (x + width, y), 1)
        
        # Helmet trim
        pygame.draw.line(surface, trim_color,
                        (helmet_x, helmet_y),
                        (helmet_x + helmet_size, helmet_y), 1)
        pygame.draw.line(surface, trim_color,
                        (helmet_x, visor_y),
                        (helmet_x + helmet_size, visor_y), 1)
                        
    def _generate_weapon(self, surface):
        """Generate knight weapons"""
        metal_color = random.choice(self.colors['metal'])
        trim_color = random.choice(self.colors['trim'])
        
        weapon_type = random.choice(['sword', 'greatsword'])
        weapon_x = 3 * self.size // 4
        weapon_y = self.size // 3
        
        if weapon_type == 'sword':
            # Blade
            pygame.draw.line(surface, metal_color,
                           (weapon_x, weapon_y),
                           (weapon_x + self.size//8, weapon_y + self.size//3), 2)
            # Handle
            pygame.draw.line(surface, (40, 30, 20),  # Dark brown
                           (weapon_x, weapon_y),
                           (weapon_x - self.size//16, weapon_y - self.size//16))
            # Crossguard
            pygame.draw.line(surface, trim_color,
                           (weapon_x - 3, weapon_y),
                           (weapon_x + 3, weapon_y), 2)
        else:  # greatsword
            # Larger blade
            pygame.draw.line(surface, metal_color,
                           (weapon_x, weapon_y - self.size//6),
                           (weapon_x + self.size//6, weapon_y + self.size//2), 3)
            # Longer handle
            pygame.draw.line(surface, (40, 30, 20),  # Dark brown
                           (weapon_x, weapon_y - self.size//6),
                           (weapon_x - self.size//12, weapon_y - self.size//4))
            # Decorative crossguard
            pygame.draw.line(surface, trim_color,
                           (weapon_x - 4, weapon_y - self.size//6),
                           (weapon_x + 4, weapon_y - self.size//6), 2)
                        
    def _add_armor_details(self, surface, x, y, width, height, detail_color):
        """Add medieval armor details"""
        # Chest emblem
        if random.random() < 0.6:  # 60% chance for emblem
            emblem_x = x + width // 2
            emblem_y = y + height // 3
            emblem_size = min(width, height) // 4
            
            emblem_type = random.choice(['cross', 'shield', 'circle'])
            if emblem_type == 'cross':
                pygame.draw.line(surface, detail_color,
                               (emblem_x, emblem_y - emblem_size),
                               (emblem_x, emblem_y + emblem_size), 1)
                pygame.draw.line(surface, detail_color,
                               (emblem_x - emblem_size, emblem_y),
                               (emblem_x + emblem_size, emblem_y), 1)
            elif emblem_type == 'shield':
                points = [
                    (emblem_x, emblem_y - emblem_size),
                    (emblem_x + emblem_size, emblem_y),
                    (emblem_x, emblem_y + emblem_size),
                    (emblem_x - emblem_size, emblem_y),
                ]
                pygame.draw.polygon(surface, detail_color, points, 1)
            else:  # circle
                pygame.draw.circle(surface, detail_color,
                                 (emblem_x, emblem_y), emblem_size, 1)
        
        # Rivets/studs
        rivet_positions = [
            (x + width//4, y + height//4),
            (x + 3*width//4, y + height//4),
            (x + width//4, y + 3*height//4),
            (x + 3*width//4, y + 3*height//4)
        ]
        
        for rx, ry in rivet_positions:
            pygame.draw.circle(surface, detail_color, (rx, ry), 1)
            
        # Edge trim
        pygame.draw.line(surface, detail_color,
                        (x, y), (x + width-1, y), 1)  # Top
        pygame.draw.line(surface, detail_color,
                        (x, y + height-1), (x + width-1, y + height-1), 1)  # Bottom 