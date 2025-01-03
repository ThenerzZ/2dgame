import pygame
import random
import math

class EquipmentSprites:
    def __init__(self, size=32):
        self.size = size
        self.colors = {
            'metal': [
                (70, 70, 80),    # Steel
                (60, 50, 40),    # Bronze
                (50, 50, 60),    # Dark silver
                (80, 70, 60),    # Copper
            ],
            'magic': [
                (100, 100, 255, 150),  # Magic blue
                (255, 100, 255, 150),  # Magic pink
                (255, 200, 100, 150),  # Magic gold
            ],
            'leather': [
                (80, 50, 20),    # Brown leather
                (60, 40, 20),    # Dark leather
                (100, 70, 40),   # Light leather
            ],
            'cloth': [
                (150, 50, 50),   # Red cloth
                (50, 50, 150),   # Blue cloth
                (150, 150, 50),  # Yellow cloth
                (50, 150, 50),   # Green cloth
            ],
            'trim': [
                (255, 215, 0),   # Gold trim
                (192, 192, 192), # Silver trim
                (176, 141, 87),  # Bronze trim
            ]
        }

    def generate_weapon_sprite(self, weapon_name):
        """Generate a weapon sprite based on the weapon type"""
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        if weapon_name == "Magic Wand":
            self._draw_magic_wand(surface)
        elif weapon_name == "Knife":
            self._draw_knife(surface)
        elif weapon_name == "Whip":
            self._draw_whip(surface)
        elif weapon_name == "Fire Wand":
            self._draw_fire_wand(surface)
        elif weapon_name == "Cross Bow":
            self._draw_crossbow(surface)
        elif weapon_name == "Lightning Ring":
            self._draw_lightning_ring(surface)
            
        return surface

    def _draw_magic_wand(self, surface):
        metal_color = random.choice(self.colors['metal'])
        magic_color = random.choice(self.colors['magic'])
        
        # Wand shaft
        pygame.draw.line(surface, metal_color,
                        (self.size//2, self.size//2),
                        (self.size//2 + 12, self.size//2), 2)
        
        # Magic crystal
        crystal_pos = (self.size//2 + 12, self.size//2)
        pygame.draw.circle(surface, magic_color[:3], crystal_pos, 3)
        
        # Glow effect
        glow_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*magic_color[:3], 100), (3, 3), 3)
        surface.blit(glow_surf, (crystal_pos[0]-3, crystal_pos[1]-3))

    def _draw_knife(self, surface):
        metal_color = random.choice(self.colors['metal'])
        handle_color = random.choice(self.colors['leather'])
        
        # Blade
        pygame.draw.polygon(surface, metal_color, [
            (self.size//2, self.size//2),
            (self.size//2 + 12, self.size//2 - 2),
            (self.size//2 + 14, self.size//2),
            (self.size//2 + 12, self.size//2 + 2),
        ])
        
        # Handle
        pygame.draw.rect(surface, handle_color,
                        (self.size//2 - 6, self.size//2 - 1, 6, 2))

    def _draw_whip(self, surface):
        leather_color = random.choice(self.colors['leather'])
        
        # Whip segments
        points = [(self.size//2, self.size//2)]
        for i in range(1, 6):
            angle = math.pi * (0.7 + i * 0.1)
            length = 4 + i * 2
            x = points[-1][0] + math.cos(angle) * length
            y = points[-1][1] + math.sin(angle) * length
            points.append((x, y))
        
        pygame.draw.lines(surface, leather_color, False, points, 2)

    def _draw_fire_wand(self, surface):
        metal_color = random.choice(self.colors['metal'])
        fire_colors = [(255, 100, 0, 150), (255, 50, 0, 100)]
        
        # Staff
        pygame.draw.line(surface, metal_color,
                        (self.size//2, self.size//2),
                        (self.size//2 + 14, self.size//2), 3)
        
        # Flame effect
        tip_pos = (self.size//2 + 14, self.size//2)
        for color in fire_colors:
            flame_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
            points = [
                (4, 0),
                (7, 3),
                (4, 7),
                (1, 3)
            ]
            pygame.draw.polygon(flame_surf, color, points)
            surface.blit(flame_surf, (tip_pos[0]-4, tip_pos[1]-4))

    def _draw_crossbow(self, surface):
        metal_color = random.choice(self.colors['metal'])
        wood_color = random.choice(self.colors['leather'])
        
        # Bow arms
        pygame.draw.arc(surface, wood_color,
                       (self.size//2, self.size//2 - 5, 10, 10),
                       -math.pi/2, math.pi/2, 2)
        
        # String
        pygame.draw.line(surface, metal_color,
                        (self.size//2 + 10, self.size//2 - 5),
                        (self.size//2 + 10, self.size//2 + 5), 1)
        
        # Stock
        pygame.draw.rect(surface, wood_color,
                        (self.size//2 - 6, self.size//2 - 1, 8, 2))

    def _draw_lightning_ring(self, surface):
        metal_color = random.choice(self.colors['metal'])
        lightning_color = (100, 150, 255, 180)
        
        # Ring
        pygame.draw.circle(surface, metal_color,
                         (self.size//2 + 8, self.size//2), 4, 1)
        
        # Lightning effect
        for _ in range(3):
            start_angle = random.uniform(0, math.pi * 2)
            points = [(self.size//2 + 8, self.size//2)]
            
            for _ in range(2):
                angle = start_angle + random.uniform(-math.pi/4, math.pi/4)
                length = random.uniform(4, 6)
                x = points[-1][0] + math.cos(angle) * length
                y = points[-1][1] + math.sin(angle) * length
                points.append((x, y))
            
            pygame.draw.lines(surface, lightning_color, False, points, 1)

    def generate_armor_overlay(self, item_name):
        """Generate armor overlay based on the item"""
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        if item_name == "Wings":
            self._draw_wings(surface)
        elif item_name == "Hollow Heart":
            self._draw_heart_armor(surface)
        elif item_name == "Bracer":
            self._draw_bracers(surface)
            
        return surface

    def _draw_wings(self, surface):
        wing_color = random.choice(self.colors['cloth'])
        alpha = 180
        
        for side in [-1, 1]:  # Left and right wings
            points = [
                (self.size//2, self.size//2),
                (self.size//2 + side * 12, self.size//2 - 8),
                (self.size//2 + side * 8, self.size//2 + 4)
            ]
            pygame.draw.polygon(surface, (*wing_color, alpha), points)

    def _draw_heart_armor(self, surface):
        armor_color = random.choice(self.colors['metal'])
        trim_color = random.choice(self.colors['trim'])
        
        # Chest plate with heart design
        pygame.draw.rect(surface, armor_color,
                        (self.size//3, self.size//3,
                         self.size//3, self.size//3))
        
        # Heart emblem
        heart_x = self.size//2
        heart_y = self.size//2
        pygame.draw.circle(surface, trim_color,
                         (heart_x - 2, heart_y), 2)
        pygame.draw.circle(surface, trim_color,
                         (heart_x + 2, heart_y), 2)
        points = [
            (heart_x - 4, heart_y),
            (heart_x + 4, heart_y),
            (heart_x, heart_y + 4)
        ]
        pygame.draw.polygon(surface, trim_color, points)

    def _draw_bracers(self, surface):
        metal_color = random.choice(self.colors['metal'])
        trim_color = random.choice(self.colors['trim'])
        
        # Left and right bracers
        for x in [self.size//4, 3*self.size//4]:
            pygame.draw.rect(surface, metal_color,
                           (x - 2, self.size//2 - 4, 4, 8))
            pygame.draw.line(surface, trim_color,
                           (x - 2, self.size//2),
                           (x + 2, self.size//2), 1) 