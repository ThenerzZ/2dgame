import pygame
import random
import math

class MonsterGenerator:
    def __init__(self, size=32):
        self.size = size
        self.colors = {
            'flesh': [
                (140, 50, 50),    # Bloody red
                (150, 100, 100),  # Pale flesh
                (80, 60, 60),     # Dark flesh
                (100, 70, 70),    # Muted flesh
            ],
            'bone': [
                (200, 190, 180),  # Ivory
                (180, 170, 160),  # Aged bone
                (160, 150, 140),  # Dark bone
            ],
            'chitin': [
                (40, 35, 30),     # Dark shell
                (60, 50, 40),     # Brown shell
                (30, 25, 20),     # Black shell
            ],
            'slime': [
                (100, 200, 50, 160),  # Toxic green
                (50, 150, 200, 160),  # Blue ooze
                (150, 50, 200, 160),  # Purple slime
            ],
            'eye': [
                (255, 50, 50),    # Red
                (255, 200, 50),   # Yellow
                (50, 255, 50),    # Green
                (50, 200, 255),   # Blue
            ],
            'magic': [
                (255, 100, 255),  # Magic pink
                (100, 200, 255),  # Magic blue
                (255, 200, 100),  # Magic gold
            ]
        }
        
        self.monster_types = [
            self._generate_skeleton,
            self._generate_slime,
            self._generate_spider,
            self._generate_demon,
            self._generate_ghost
        ]
        
        self.death_animations = [
            self._generate_skeleton_death,  # NORMAL
            self._generate_slime_death,     # WEAK
            self._generate_spider_death,    # STRONG
            self._generate_demon_death,     # ELITE
            self._generate_ghost_death      # BOSS
        ]

    def generate_monster(self, monster_type=None):
        """Generate a random monster sprite with death animation frames"""
        if monster_type is None:
            generator = random.choice(self.monster_types)
            death_generator = random.choice(self.death_animations)
        else:
            generator = self.monster_types[monster_type]
            death_generator = self.death_animations[monster_type]
            
        sprite = generator(pygame.Surface((self.size, self.size), pygame.SRCALPHA))
        death_frames = death_generator()
        return sprite, death_frames

    def _generate_skeleton(self, surface):
        """Generate an undead skeleton warrior"""
        bone_color = random.choice(self.colors['bone'])
        eye_color = random.choice(self.colors['eye'])
        
        # Skull
        skull_size = self.size // 3
        skull_x = (self.size - skull_size) // 2
        skull_y = self.size // 4
        
        pygame.draw.rect(surface, bone_color,
                        (skull_x, skull_y, skull_size, skull_size))
        
        # Glowing eyes
        eye_size = 2
        left_eye = (skull_x + skull_size//3, skull_y + skull_size//2)
        right_eye = (skull_x + 2*skull_size//3, skull_y + skull_size//2)
        
        for eye_pos in [left_eye, right_eye]:
            # Glow effect
            pygame.draw.circle(surface, (*eye_color[:3], 100),
                             eye_pos, eye_size + 1)
            # Eye core
            pygame.draw.circle(surface, eye_color,
                             eye_pos, eye_size)
        
        # Ribcage
        rib_width = self.size // 2
        rib_start_y = skull_y + skull_size + 2
        for i in range(4):
            y = rib_start_y + i * 3
            pygame.draw.line(surface, bone_color,
                           (self.size//2 - rib_width//2, y),
                           (self.size//2 + rib_width//2, y))
        
        # Arms (bones)
        arm_y = rib_start_y + 2
        for x in [self.size//3, 2*self.size//3]:
            pygame.draw.line(surface, bone_color,
                           (x, arm_y),
                           (x, arm_y + self.size//3), 2)
        
        return surface

    def _generate_slime(self, surface):
        """Generate a gelatinous slime creature"""
        slime_color = random.choice(self.colors['slime'])
        eye_color = random.choice(self.colors['eye'])
        
        # Main body (bouncy shape)
        height = int(self.size * 0.7)
        width = int(self.size * 0.8)
        x = (self.size - width) // 2
        y = self.size - height
        
        # Draw multiple layers for transparency effect
        for i in range(3):
            offset = i * 2
            alpha = 160 - i * 40
            color = (*slime_color[:3], alpha)
            
            points = [
                (x + offset, y + height - offset),
                (x + width - offset, y + height - offset),
                (x + width - offset//2, y + offset),
                (x + offset//2, y + offset)
            ]
            pygame.draw.polygon(surface, color, points)
        
        # Eyes (1-3 random eyes)
        num_eyes = random.randint(1, 3)
        eye_positions = []
        
        for _ in range(num_eyes):
            eye_x = random.randint(x + width//4, x + 3*width//4)
            eye_y = random.randint(y + height//3, y + 2*height//3)
            eye_positions.append((eye_x, eye_y))
        
        for eye_pos in eye_positions:
            pygame.draw.circle(surface, eye_color, eye_pos, 2)
            pygame.draw.circle(surface, (255, 255, 255), 
                             (eye_pos[0]-1, eye_pos[1]-1), 1)
        
        return surface

    def _generate_spider(self, surface):
        """Generate a giant spider"""
        chitin_color = random.choice(self.colors['chitin'])
        eye_color = random.choice(self.colors['eye'])
        
        # Body segments
        body_width = self.size // 2
        body_height = self.size // 3
        body_x = (self.size - body_width) // 2
        body_y = self.size // 3
        
        # Abdomen (back part)
        pygame.draw.ellipse(surface, chitin_color,
                          (body_x, body_y, body_width, body_height))
        
        # Thorax (front part)
        thorax_size = body_height
        pygame.draw.circle(surface, chitin_color,
                         (body_x, body_y + body_height//2),
                         thorax_size//2)
        
        # Eyes (4 pairs)
        eye_size = 1
        base_x = body_x - thorax_size//3
        base_y = body_y + body_height//2 - thorax_size//3
        
        for i in range(4):
            x_offset = i * 3
            y_offset = abs(i - 1.5) * 2
            
            # Left eye
            pygame.draw.circle(surface, eye_color,
                             (base_x + x_offset, base_y + y_offset), eye_size)
            # Right eye
            pygame.draw.circle(surface, eye_color,
                             (base_x + x_offset + 6, base_y + y_offset), eye_size)
        
        # Legs (4 pairs)
        for i in range(4):
            y_base = body_y + body_height//3 + i * (body_height//4)
            
            # Left leg
            points_l = [
                (body_x, y_base),
                (body_x - body_width//2, y_base - 3),
                (body_x - body_width//2 - 2, y_base + 3)
            ]
            pygame.draw.lines(surface, chitin_color, False, points_l, 1)
            
            # Right leg
            points_r = [
                (body_x + body_width, y_base),
                (body_x + body_width * 1.5, y_base - 3),
                (body_x + body_width * 1.5 + 2, y_base + 3)
            ]
            pygame.draw.lines(surface, chitin_color, False, points_r, 1)
        
        return surface

    def _generate_demon(self, surface):
        """Generate a demon creature"""
        flesh_color = random.choice(self.colors['flesh'])
        eye_color = (255, 50, 50)  # Always red for demons
        magic_color = random.choice(self.colors['magic'])
        
        # Horned head
        head_size = self.size // 3
        head_x = (self.size - head_size) // 2
        head_y = self.size // 4
        
        pygame.draw.rect(surface, flesh_color,
                        (head_x, head_y, head_size, head_size))
        
        # Horns
        horn_length = head_size // 2
        for x_offset in [-2, head_size + 2]:
            points = [
                (head_x + x_offset, head_y + 2),
                (head_x + x_offset + (-2 if x_offset < 0 else 2), head_y - horn_length),
                (head_x + x_offset + (-1 if x_offset < 0 else 1), head_y)
            ]
            pygame.draw.polygon(surface, flesh_color, points)
        
        # Glowing eyes
        eye_size = 2
        pygame.draw.circle(surface, (*eye_color, 160),
                         (head_x + head_size//3, head_y + head_size//2),
                         eye_size + 1)
        pygame.draw.circle(surface, eye_color,
                         (head_x + 2*head_size//3, head_y + head_size//2),
                         eye_size)
        
        # Muscular body
        body_width = self.size // 2
        body_height = self.size // 2
        body_x = (self.size - body_width) // 2
        body_y = head_y + head_size
        
        pygame.draw.rect(surface, flesh_color,
                        (body_x, body_y, body_width, body_height))
        
        # Magic runes
        for _ in range(3):
            rune_x = random.randint(body_x, body_x + body_width - 4)
            rune_y = random.randint(body_y, body_y + body_height - 4)
            self._draw_rune(surface, rune_x, rune_y, magic_color)
        
        # Wings
        wing_width = self.size // 3
        wing_height = self.size // 2
        for x_offset in [-wing_width + 4, body_width - 4]:
            points = [
                (body_x + x_offset, body_y),
                (body_x + x_offset + wing_width, body_y - wing_height//2),
                (body_x + x_offset + wing_width//2, body_y)
            ]
            pygame.draw.polygon(surface, flesh_color, points)
        
        return surface

    def _generate_ghost(self, surface):
        """Generate a spectral ghost"""
        # Base ghost colors with alpha
        ghost_colors = [
            (200, 200, 255, 60),  # Ethereal blue
            (200, 255, 200, 60),  # Ethereal green
            (255, 200, 255, 60),  # Ethereal purple
        ]
        ghost_color = random.choice(ghost_colors)
        eye_color = random.choice(self.colors['eye'])
        
        # Multiple transparent layers for ethereal effect
        for i in range(3):
            offset = i * 2
            alpha = ghost_color[3] - i * 20
            
            # Main spectral shape
            height = int(self.size * 0.8)
            width = int(self.size * 0.6)
            x = (self.size - width) // 2
            y = self.size // 4
            
            # Wavy bottom
            points = [(x + offset, y)]
            for w in range(width - 2*offset):
                wave = math.sin(w * 0.5) * 3
                points.append((x + w + offset, y + height + wave))
            points.append((x + width - offset, y))
            
            color = (*ghost_color[:3], alpha)
            pygame.draw.polygon(surface, color, points)
        
        # Glowing eyes
        eye_size = 2
        eye_y = self.size // 2
        left_x = self.size//2 - 5
        right_x = self.size//2 + 5
        
        for eye_x in [left_x, right_x]:
            # Outer glow
            pygame.draw.circle(surface, (*eye_color[:3], 100),
                             (eye_x, eye_y), eye_size + 1)
            # Inner bright part
            pygame.draw.circle(surface, (*eye_color[:3], 200),
                             (eye_x, eye_y), eye_size)
        
        return surface

    def _draw_rune(self, surface, x, y, color):
        """Helper method to draw magical runes"""
        rune_types = [
            [(0,0), (3,0), (1,3)],  # Triangle
            [(0,0), (3,0), (3,3), (0,3)],  # Square
            [(0,2), (2,0), (4,2)],  # Peak
            [(2,0), (0,2), (4,2)],  # V shape
        ]
        
        points = random.choice(rune_types)
        adjusted_points = [(x + px, y + py) for px, py in points]
        pygame.draw.lines(surface, color, True, adjusted_points, 1) 

    def _generate_skeleton_death(self):
        """Generate skeleton death animation frames"""
        frames = []
        
        # Frame 1: Initial collapse
        frame1 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self._generate_skeleton(frame1)
        frame1 = pygame.transform.rotate(frame1, -15)  # Slight tilt
        frames.append(frame1)
        
        # Frame 2: Breaking apart
        frame2 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        bone_color = random.choice(self.colors['bone'])
        # Draw scattered bones
        for i in range(4):
            x = self.size//2 + random.randint(-5, 5)
            y = self.size//2 + random.randint(-5, 5)
            pygame.draw.ellipse(frame2, bone_color, (x, y, 4, 2))
        frames.append(frame2)
        
        # Frame 3: Final scattered bones
        frame3 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        for i in range(6):
            x = self.size//2 + random.randint(-8, 8)
            y = self.size//2 + random.randint(-8, 8)
            pygame.draw.ellipse(frame3, bone_color, (x, y, 4, 2))
        frames.append(frame3)
        
        return frames

    def _generate_slime_death(self):
        """Generate slime death animation frames"""
        frames = []
        
        # Frame 1: Initial splat
        frame1 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self._generate_slime(frame1)
        frame1 = pygame.transform.scale(frame1, (self.size, int(self.size * 0.8)))
        frames.append(frame1)
        
        # Frame 2: Wider splat
        frame2 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        slime_color = random.choice(self.colors['slime'])
        pygame.draw.ellipse(frame2, slime_color, (0, self.size//2, self.size, self.size//4))
        frames.append(frame2)
        
        # Frame 3: Final puddle
        frame3 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.ellipse(frame3, (*slime_color[:3], 128), 
                          (2, self.size//2 + 2, self.size-4, self.size//6))
        frames.append(frame3)
        
        return frames

    def _generate_spider_death(self):
        """Generate spider death animation frames"""
        frames = []
        
        # Frame 1: Legs curling
        frame1 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self._generate_spider(frame1)
        frame1 = pygame.transform.rotate(frame1, 20)
        frames.append(frame1)
        
        # Frame 2: Curled up
        frame2 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        chitin_color = random.choice(self.colors['chitin'])
        # Draw curled body
        pygame.draw.circle(frame2, chitin_color, (self.size//2, self.size//2), self.size//4)
        # Draw curled legs
        for i in range(4):
            angle = i * math.pi/2
            x = self.size//2 + math.cos(angle) * self.size//4
            y = self.size//2 + math.sin(angle) * self.size//4
            pygame.draw.arc(frame2, chitin_color, 
                          (x-2, y-2, 4, 4), 0, math.pi, 1)
        frames.append(frame2)
        
        # Frame 3: Final curled state
        frame3 = frame2.copy()
        frame3.set_alpha(200)
        frames.append(frame3)
        
        return frames

    def _generate_demon_death(self):
        """Generate demon death animation frames"""
        frames = []
        
        # Frame 1: Initial burn
        frame1 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self._generate_demon(frame1)
        # Add fire overlay
        for _ in range(5):
            x = random.randint(0, self.size)
            y = random.randint(0, self.size)
            pygame.draw.circle(frame1, (255, 100, 0, 128), (x, y), 2)
        frames.append(frame1)
        
        # Frame 2: More intense burn
        frame2 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self._generate_demon(frame2)
        frame2.fill((255, 100, 0, 100), special_flags=pygame.BLEND_RGBA_ADD)
        frames.append(frame2)
        
        # Frame 3: Final burn
        frame3 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        for _ in range(10):
            x = random.randint(0, self.size)
            y = random.randint(0, self.size)
            pygame.draw.circle(frame3, (255, 50, 0, 150), (x, y), 3)
        frames.append(frame3)
        
        return frames

    def _generate_ghost_death(self):
        """Generate ghost death animation frames"""
        frames = []
        
        # Frame 1: Initial fade
        frame1 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self._generate_ghost(frame1)
        frame1.set_alpha(200)
        frames.append(frame1)
        
        # Frame 2: Distortion
        frame2 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self._generate_ghost(frame2)
        frame2 = pygame.transform.scale(frame2, (int(self.size * 1.2), self.size))
        frame2.set_alpha(150)
        frames.append(frame2)
        
        # Frame 3: Final dissipate
        frame3 = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        ghost_color = random.choice(self.colors['slime'])
        for _ in range(8):
            x = random.randint(0, self.size)
            y = random.randint(0, self.size)
            pygame.draw.circle(frame3, (*ghost_color[:3], 100), (x, y), 2)
        frames.append(frame3)
        
        return frames 