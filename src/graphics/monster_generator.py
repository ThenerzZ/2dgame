import pygame
import random
import numpy
import math
from game.monster_config import MonsterType, get_monster_config, get_monster_colors

class MonsterGenerator:
    def __init__(self, size):
        self.size = size
        self.surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
    def generate_monster(self, monster_type_index):
        """Generate monster sprite and death animation frames based on type"""
        monster_type = list(MonsterType)[monster_type_index]
        config = get_monster_config(monster_type)
        colors = get_monster_colors(monster_type)
        sprite_config = config["sprite_config"]
        
        # Generate main sprite
        sprite = self._generate_sprite(monster_type, sprite_config, colors)
        
        # Generate death animation frames
        death_frames = self._generate_death_frames(monster_type, sprite)
        
        return sprite, death_frames
        
    def _generate_sprite(self, monster_type, sprite_config, colors):
        """Generate the main sprite based on monster type configuration"""
        self.surface.fill((0, 0, 0, 0))
        
        if monster_type == MonsterType.SKELETON:
            self._draw_skeleton(sprite_config, colors)
        elif monster_type == MonsterType.SLIME:
            self._draw_slime(sprite_config, colors)
        elif monster_type == MonsterType.SPIDER:
            self._draw_spider(sprite_config, colors)
        elif monster_type == MonsterType.DEMON:
            self._draw_demon(sprite_config, colors)
        elif monster_type == MonsterType.GHOST:
            self._draw_ghost(sprite_config, colors)
        elif monster_type == MonsterType.RAT:
            self._draw_rat(sprite_config, colors)
        elif monster_type == MonsterType.BAT:
            self._draw_bat(sprite_config, colors)
        elif monster_type == MonsterType.ZOMBIE:
            self._draw_zombie(sprite_config, colors)
        elif monster_type == MonsterType.GOLEM:
            self._draw_golem(sprite_config, colors)
        elif monster_type == MonsterType.WITCH:
            self._draw_witch(sprite_config, colors)
        elif monster_type == MonsterType.DRAGON:
            self._draw_dragon(sprite_config, colors)
        elif monster_type == MonsterType.NECROMANCER:
            self._draw_necromancer(sprite_config, colors)
        elif monster_type == MonsterType.VAMPIRE:
            self._draw_vampire(sprite_config, colors)
        elif monster_type == MonsterType.DEMON_LORD:
            self._draw_demon_lord(sprite_config, colors)
        elif monster_type == MonsterType.LICH:
            self._draw_lich(sprite_config, colors)
            
        return self.surface.copy()
        
    def _generate_death_frames(self, monster_type, base_sprite):
        """Generate death animation frames based on monster type"""
        config = get_monster_config(monster_type)
        death_config = config["death_animation"]
        frames = []
        
        for i in range(death_config["frame_count"]):
            frame = base_sprite.copy()
            progress = i / (death_config["frame_count"] - 1)
            
            if "scatter" in death_config["effects"]:
                self._apply_scatter_effect(frame, progress)
            if "splat" in death_config["effects"]:
                self._apply_splat_effect(frame, progress)
            if "curl" in death_config["effects"]:
                self._apply_curl_effect(frame, progress)
            if "burn" in death_config["effects"]:
                self._apply_burn_effect(frame, progress)
            if "dissipate" in death_config["effects"]:
                self._apply_dissipate_effect(frame, progress)
            if "fade" in death_config["effects"]:
                self._apply_fade_effect(frame, progress)
                
            frames.append(frame)
            
        return frames
        
    def _draw_skeleton(self, config, colors):
        """Draw skeleton sprite parts with more detail"""
        parts = config["parts"]
        ratios = config["size_ratio"]
        
        if "skull" in parts:
            # Skull base
            skull_size = int(self.size * ratios["skull"])
            skull_x = self.size//3
            skull_y = self.size//4
            pygame.draw.ellipse(self.surface, colors["primary"][0],
                              (skull_x, skull_y, skull_size, skull_size))
            
            # Eyes (glowing)
            eye_size = skull_size // 4
            eye_spacing = skull_size // 3
            for x in [skull_x + skull_size//3, skull_x + 2*skull_size//3]:
                # Outer glow
                pygame.draw.circle(self.surface, (*colors["secondary"][0][:3], 100),
                                (x, skull_y + skull_size//2), eye_size)
                # Inner eye
                pygame.draw.circle(self.surface, colors["secondary"][0],
                                (x, skull_y + skull_size//2), eye_size//2)
            
            # Jaw details
            jaw_points = [
                (skull_x, skull_y + skull_size - 2),
                (skull_x + skull_size//3, skull_y + skull_size),
                (skull_x + 2*skull_size//3, skull_y + skull_size),
                (skull_x + skull_size, skull_y + skull_size - 2)
            ]
            pygame.draw.lines(self.surface, colors["primary"][1], False, jaw_points, 2)
            
        if "ribcage" in parts:
            # Spine
            spine_x = self.size//2
            spine_y = skull_y + skull_size
            spine_height = int(self.size * ratios["ribcage"])
            pygame.draw.line(self.surface, colors["primary"][1],
                           (spine_x, spine_y),
                           (spine_x, spine_y + spine_height), 3)
            
            # Ribs
            for i in range(4):
                y = spine_y + (i * spine_height//4)
                # Left rib
                pygame.draw.arc(self.surface, colors["primary"][1],
                              (spine_x - self.size//4, y, self.size//4, spine_height//4),
                              0, math.pi/2, 2)
                # Right rib
                pygame.draw.arc(self.surface, colors["primary"][1],
                              (spine_x, y, self.size//4, spine_height//4),
                              math.pi/2, math.pi, 2)
            
        if "arms" in parts:
            # Arms with joints
            arm_length = int(self.size * ratios["arms"])
            for x_offset in [-arm_length//2, arm_length//2]:
                # Upper arm
                start_pos = (self.size//2 + x_offset//2, spine_y + spine_height//3)
                mid_pos = (self.size//2 + x_offset, spine_y + spine_height//2)
                pygame.draw.line(self.surface, colors["primary"][2],
                               start_pos, mid_pos, 2)
                # Lower arm
                end_pos = (mid_pos[0], mid_pos[1] + arm_length//2)
                pygame.draw.line(self.surface, colors["primary"][2],
                               mid_pos, end_pos, 2)
                # Joint
                pygame.draw.circle(self.surface, colors["primary"][1],
                                mid_pos, 2)
            
    def _draw_slime(self, config, colors):
        """Draw slime sprite with wobble effect"""
        body_size = int(self.size * config["size_ratio"]["body"])
        
        # Multiple translucent layers for depth
        for i in range(3):
            size_mod = body_size - i * 4
            alpha = 160 - i * 40
            color = (*colors["primary"][0][:3], alpha)
            
            # Wobble effect using sine wave
            points = []
            segments = 12
            for j in range(segments + 1):
                angle = (j / segments) * 2 * math.pi
                wobble = math.sin(angle * 3 + i) * 2
                x = self.size//2 + math.cos(angle) * (size_mod//2 + wobble)
                y = self.size//2 + math.sin(angle) * (size_mod//2 + wobble)
                points.append((x, y))
            
            pygame.draw.polygon(self.surface, color, points)
        
        # Eyes (1-3 random eyes)
        num_eyes = random.randint(1, 3)
        eye_color = colors["primary"][0]  # Use a contrasting color
        for _ in range(num_eyes):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(2, body_size//4)
            x = self.size//2 + math.cos(angle) * distance
            y = self.size//2 + math.sin(angle) * distance
            
            # Eye shine
            pygame.draw.circle(self.surface, (255, 255, 255),
                             (x, y), 3)
            pygame.draw.circle(self.surface, eye_color,
                             (x, y), 2)
            
    def _draw_spider(self, config, colors):
        """Draw spider with detailed legs and body"""
        body_size = int(self.size * config["size_ratio"]["body"])
        leg_length = int(self.size * config["size_ratio"]["legs"])
        
        # Abdomen (back part)
        pygame.draw.ellipse(self.surface, colors["primary"][0],
                          (self.size//2 - body_size//2, self.size//3, 
                           body_size, body_size))
        
        # Thorax (front part)
        thorax_size = body_size * 2//3
        pygame.draw.circle(self.surface, colors["primary"][1],
                         (self.size//2, self.size//2), thorax_size//2)
        
        # Legs (4 pairs, jointed)
        for i in range(8):
            angle = (i / 8) * 2 * math.pi + math.pi/8
            # Leg segments
            start_x = self.size//2
            start_y = self.size//2
            
            # First segment
            mid1_x = start_x + math.cos(angle) * leg_length//2
            mid1_y = start_y + math.sin(angle) * leg_length//2
            pygame.draw.line(self.surface, colors["primary"][2],
                           (start_x, start_y), (mid1_x, mid1_y), 2)
            
            # Second segment
            end_x = mid1_x + math.cos(angle + math.pi/6) * leg_length//2
            end_y = mid1_y + math.sin(angle + math.pi/6) * leg_length//2
            pygame.draw.line(self.surface, colors["primary"][2],
                           (mid1_x, mid1_y), (end_x, end_y), 2)
            
            # Joint
            pygame.draw.circle(self.surface, colors["primary"][1],
                            (mid1_x, mid1_y), 2)
        
        # Eyes (4 pairs)
        eye_size = 2
        eye_spacing = 3
        base_y = self.size//2 - thorax_size//4
        for i in range(4):
            x_offset = i * eye_spacing - (eye_spacing * 1.5)
            y_offset = abs(i - 1.5) * 2
            
            # Left eye
            pygame.draw.circle(self.surface, (255, 255, 255),
                             (self.size//2 + x_offset, base_y + y_offset), eye_size)
            pygame.draw.circle(self.surface, colors["primary"][0],
                             (self.size//2 + x_offset, base_y + y_offset), eye_size-1)
            
            # Right eye
            pygame.draw.circle(self.surface, (255, 255, 255),
                             (self.size//2 - x_offset, base_y + y_offset), eye_size)
            pygame.draw.circle(self.surface, colors["primary"][0],
                             (self.size//2 - x_offset, base_y + y_offset), eye_size-1)
            
    def _draw_demon(self, config, colors):
        """Draw demon with detailed features and effects"""
        body_size = int(self.size * config["size_ratio"]["body"])
        horn_size = int(self.size * config["size_ratio"]["horns"])
        wing_size = int(self.size * config["size_ratio"]["wings"])
        
        # Wings (with detail)
        for x_offset in [-1, 1]:
            wing_points = [
                (self.size//2, self.size//2),  # Base
                (self.size//2 + x_offset * wing_size, self.size//3),  # Top
                (self.size//2 + x_offset * wing_size * 1.2, self.size//2),  # Middle
                (self.size//2 + x_offset * wing_size, self.size*2//3),  # Bottom
            ]
            pygame.draw.polygon(self.surface, colors["secondary"][0], wing_points)
            
            # Wing details
            for i in range(3):
                start = wing_points[0]
                end = wing_points[i + 1]
                pygame.draw.line(self.surface, colors["secondary"][1],
                               start, end, 1)
        
        # Body
        pygame.draw.rect(self.surface, colors["primary"][0],
                        (self.size//2 - body_size//2, self.size//3, 
                         body_size, body_size))
        
        # Horns
        for x_offset in [-1, 1]:
            horn_points = [
                (self.size//2 + x_offset * horn_size//2, self.size//3),  # Base
                (self.size//2 + x_offset * horn_size, self.size//4),  # Tip
                (self.size//2 + x_offset * horn_size*0.8, self.size//3 + horn_size//4),  # Back
            ]
            pygame.draw.polygon(self.surface, colors["primary"][1], horn_points)
        
        # Eyes (glowing)
        eye_size = body_size//6
        for x_offset in [-1, 1]:
            eye_pos = (self.size//2 + x_offset * body_size//3, 
                      self.size//2)
            # Outer glow
            pygame.draw.circle(self.surface, (*colors["secondary"][0][:3], 100),
                             eye_pos, eye_size)
            # Inner eye
            pygame.draw.circle(self.surface, colors["secondary"][0],
                             eye_pos, eye_size//2)
        
        # Runes
        for _ in range(3):
            x = random.randint(self.size//2 - body_size//3, 
                             self.size//2 + body_size//3)
            y = random.randint(self.size//2, self.size//2 + body_size//2)
            self._draw_rune(x, y, colors["secondary"][1])
            
    def _draw_ghost(self, config, colors):
        """Draw ghost with ethereal effects"""
        body_size = int(self.size * config["size_ratio"]["body"])
        aura_size = int(self.size * config["size_ratio"]["aura"])
        
        # Multiple ethereal layers
        for i in range(3):
            size = aura_size - i * 4
            alpha = 100 - i * 30
            
            # Wavy bottom effect
            points = [(self.size//2, self.size//3)]  # Top point
            segments = 12
            for j in range(segments + 1):
                progress = j / segments
                wave = math.sin(progress * math.pi * 2) * 4
                x = self.size//2 + (progress - 0.5) * size
                y = self.size//2 + size//2 + wave
                points.append((x, y))
            
            color = (*colors["primary"][0][:3], alpha)
            pygame.draw.polygon(self.surface, color, points)
        
        # Core body (more solid)
        pygame.draw.circle(self.surface, colors["primary"][0],
                         (self.size//2, self.size//2), body_size//2)
        
        # Eyes (ethereal glow)
        eye_size = body_size//6
        for x_offset in [-1, 1]:
            eye_pos = (self.size//2 + x_offset * body_size//3, 
                      self.size//2)
            # Outer glow
            pygame.draw.circle(self.surface, (*colors["primary"][1][:3], 100),
                             eye_pos, eye_size)
            # Inner eye
            pygame.draw.circle(self.surface, colors["primary"][1],
                             eye_pos, eye_size//2)
            # Eye shine
            pygame.draw.circle(self.surface, (255, 255, 255, 200),
                             (eye_pos[0] - 1, eye_pos[1] - 1), eye_size//4)
            
    def _draw_rune(self, x, y, color):
        """Draw a magical rune"""
        size = 4
        rune_types = [
            [(0,0), (size,0), (size/2,size)],  # Triangle
            [(0,0), (size,0), (size,size), (0,size)],  # Square
            [(size/2,0), (0,size), (size,size)],  # Triangle pointing down
            [(0,size/2), (size/2,0), (size,size/2), (size/2,size)],  # Diamond
        ]
        
        points = random.choice(rune_types)
        adjusted_points = [(x + px, y + py) for px, py in points]
        pygame.draw.polygon(self.surface, color, adjusted_points)
        # Glow effect
        glow_color = (*color[:3], 100)
        pygame.draw.polygon(self.surface, glow_color, adjusted_points)
        
    def _apply_scatter_effect(self, surface, progress):
        """Apply scatter effect for skeleton death"""
        displacement = int(progress * self.size * 0.3)
        pixels = pygame.surfarray.pixels_alpha(surface)
        pixels[displacement:, :] = pixels[:-displacement, :] if displacement > 0 else pixels
        del pixels
        
    def _apply_splat_effect(self, surface, progress):
        """Apply splat effect for slime death"""
        squish = 1 - progress * 0.8
        scaled = pygame.transform.scale(surface, 
                                     (surface.get_width(), 
                                      int(surface.get_height() * squish)))
        surface.fill((0, 0, 0, 0))
        surface.blit(scaled, (0, surface.get_height() - scaled.get_height()))
        
    def _apply_curl_effect(self, surface, progress):
        """Apply curl effect for spider death"""
        scale = 1 - progress * 0.5
        angle = progress * 180
        scaled = pygame.transform.scale(surface,
                                     (int(surface.get_width() * scale),
                                      int(surface.get_height() * scale)))
        rotated = pygame.transform.rotate(scaled, angle)
        surface.fill((0, 0, 0, 0))
        surface.blit(rotated,
                    (surface.get_width()//2 - rotated.get_width()//2,
                     surface.get_height()//2 - rotated.get_height()//2))
        
    def _apply_burn_effect(self, surface, progress):
        """Apply burn effect for demon death"""
        pixels = pygame.surfarray.pixels_alpha(surface)
        noise = (numpy.random.rand(*pixels.shape) * 255 * progress).astype(numpy.uint8)
        pixels[:] = numpy.minimum(pixels, 255 - noise)
        del pixels
        
    def _apply_dissipate_effect(self, surface, progress):
        """Apply dissipate effect for ghost death"""
        pixels = pygame.surfarray.pixels_alpha(surface)
        mask = (numpy.random.rand(*pixels.shape) > progress)
        pixels[:] = pixels * mask
        del pixels
        
    def _apply_fade_effect(self, surface, progress):
        """Apply fade effect for all deaths"""
        surface.set_alpha(int(255 * (1 - progress))) 
        
    def _draw_rat(self, config, colors):
        """Draw rat sprite with details"""
        parts = config["parts"]
        ratios = config["size_ratio"]
        
        # Body
        body_size = int(self.size * ratios["body"])
        pygame.draw.ellipse(self.surface, colors["primary"][0],
                          (self.size//3, self.size//3, body_size, body_size//2))
        
        # Tail
        tail_length = int(self.size * ratios["tail"])
        tail_points = [
            (self.size//3 + body_size, self.size//2),
            (self.size//3 + body_size + tail_length//2, self.size//2 - tail_length//4),
            (self.size//3 + body_size + tail_length, self.size//2)
        ]
        pygame.draw.lines(self.surface, colors["primary"][1], False, tail_points, 2)
        
        # Ears
        ear_size = int(self.size * ratios["ears"])
        for x_offset in [-ear_size//2, ear_size//2]:
            pygame.draw.polygon(self.surface, colors["primary"][0],
                              [(self.size//3 + ear_size + x_offset, self.size//3),
                               (self.size//3 + ear_size + x_offset - ear_size//2, self.size//3 - ear_size),
                               (self.size//3 + ear_size + x_offset + ear_size//2, self.size//3 - ear_size)])
        
        # Eyes (red)
        eye_size = 2
        for x_offset in [-4, 4]:
            pygame.draw.circle(self.surface, colors["secondary"][0],
                             (self.size//3 + ear_size + x_offset, self.size//3 + ear_size//2), eye_size)
            
    def _draw_bat(self, config, colors):
        """Draw bat sprite with wing animation"""
        parts = config["parts"]
        ratios = config["size_ratio"]
        
        # Body
        body_size = int(self.size * ratios["body"])
        pygame.draw.ellipse(self.surface, colors["primary"][0],
                          (self.size//2 - body_size//2, self.size//2 - body_size//2,
                           body_size, body_size))
        
        # Wings
        wing_size = int(self.size * ratios["wings"])
        for x_offset in [-1, 1]:
            # Wing membrane
            points = [
                (self.size//2, self.size//2),  # Center
                (self.size//2 + x_offset * wing_size, self.size//3),  # Top
                (self.size//2 + x_offset * wing_size, self.size*2//3),  # Bottom
            ]
            pygame.draw.polygon(self.surface, colors["primary"][1], points)
            
            # Wing bones
            pygame.draw.line(self.surface, colors["primary"][0],
                           points[0], points[1], 1)
            pygame.draw.line(self.surface, colors["primary"][0],
                           points[0], points[2], 1)
        
        # Eyes
        eye_size = 2
        for x_offset in [-3, 3]:
            pygame.draw.circle(self.surface, colors["secondary"][0],
                             (self.size//2 + x_offset, self.size//2), eye_size)
            
    def _draw_zombie(self, config, colors):
        """Draw zombie with decaying features"""
        parts = config["parts"]
        ratios = config["size_ratio"]
        
        # Body
        body_size = int(self.size * ratios["body"])
        pygame.draw.rect(self.surface, colors["primary"][0],
                        (self.size//3, self.size//3, body_size, body_size))
        
        # Arms (hanging)
        arm_length = int(self.size * ratios["arms"])
        for x_offset in [-2, body_size + 2]:
            start_pos = (self.size//3 + x_offset, self.size//3 + body_size//3)
            end_pos = (start_pos[0], start_pos[1] + arm_length)
            pygame.draw.line(self.surface, colors["primary"][1],
                           start_pos, end_pos, 3)
        
        # Head (tilted)
        head_size = int(self.size * ratios["head"])
        pygame.draw.rect(self.surface, colors["primary"][0],
                        (self.size//3 + body_size//4, self.size//4, head_size, head_size))
        
        # Eyes
        eye_size = 2
        eye_y = self.size//4 + head_size//2
        for x_offset in [-3, 3]:
            eye_x = self.size//3 + body_size//4 + head_size//2 + x_offset
            pygame.draw.circle(self.surface, colors["secondary"][0],
                             (eye_x, eye_y), eye_size)
            
    def _draw_golem(self, config, colors):
        """Draw stone golem with glowing runes"""
        parts = config["parts"]
        ratios = config["size_ratio"]
        
        # Body
        body_size = int(self.size * ratios["body"])
        pygame.draw.rect(self.surface, colors["primary"][0],
                        (self.size//4, self.size//4, body_size, body_size))
        
        # Arms
        arm_size = int(self.size * ratios["arms"])
        for x_offset in [-arm_size, body_size]:
            pygame.draw.rect(self.surface, colors["primary"][1],
                           (self.size//4 + x_offset, self.size//3,
                            arm_size, body_size//2))
        
        # Core (glowing)
        core_size = int(self.size * ratios["core"])
        core_pos = (self.size//4 + body_size//2 - core_size//2,
                   self.size//4 + body_size//2 - core_size//2)
        
        # Outer glow
        pygame.draw.circle(self.surface, (*colors["secondary"][0][:3], 100),
                         (core_pos[0] + core_size//2, core_pos[1] + core_size//2),
                         core_size * 0.7)
        # Inner core
        pygame.draw.circle(self.surface, colors["secondary"][0],
                         (core_pos[0] + core_size//2, core_pos[1] + core_size//2),
                         core_size//2)
        
        # Runes
        for _ in range(4):
            x = random.randint(self.size//4, self.size//4 + body_size)
            y = random.randint(self.size//4, self.size//4 + body_size)
            self._draw_rune(x, y, colors["secondary"][0])
            
    def _draw_witch(self, config, colors):
        """Draw witch with magical effects"""
        parts = config["parts"]
        ratios = config["size_ratio"]
        
        # Body (robe)
        body_size = int(self.size * ratios["body"])
        points = [
            (self.size//3, self.size//3),  # Top
            (self.size//3 + body_size, self.size//3),  # Top right
            (self.size//3 + body_size * 1.2, self.size//3 + body_size),  # Bottom right
            (self.size//3 - body_size * 0.2, self.size//3 + body_size),  # Bottom left
        ]
        pygame.draw.polygon(self.surface, colors["primary"][0], points)
        
        # Hat
        hat_size = int(self.size * ratios["hat"])
        hat_points = [
            (self.size//3, self.size//3),  # Base left
            (self.size//3 + body_size, self.size//3),  # Base right
            (self.size//3 + body_size//2, self.size//3 - hat_size),  # Tip
        ]
        pygame.draw.polygon(self.surface, colors["primary"][1], hat_points)
        
        # Staff
        staff_length = int(self.size * ratios["staff"])
        staff_start = (self.size//3 + body_size, self.size//3 + body_size//2)
        staff_end = (staff_start[0] + staff_length//2, staff_start[1] - staff_length)
        pygame.draw.line(self.surface, colors["secondary"][0],
                        staff_start, staff_end, 2)
        
        # Staff orb
        orb_pos = (staff_end[0], staff_end[1])
        pygame.draw.circle(self.surface, (*colors["secondary"][0][:3], 100),
                         orb_pos, 6)  # Outer glow
        pygame.draw.circle(self.surface, colors["secondary"][0],
                         orb_pos, 4)  # Inner orb
            
    def _draw_dragon(self, config, colors):
        """Draw dragon with impressive features"""
        parts = config["parts"]
        ratios = config["size_ratio"]
        
        # Wings
        wing_size = int(self.size * ratios["wings"])
        for x_offset in [-1, 1]:
            points = [
                (self.size//2, self.size//2),  # Base
                (self.size//2 + x_offset * wing_size, self.size//3),  # Top
                (self.size//2 + x_offset * wing_size * 1.2, self.size//2),  # Middle
                (self.size//2 + x_offset * wing_size, self.size*2//3),  # Bottom
            ]
            pygame.draw.polygon(self.surface, colors["primary"][0], points)
            
            # Wing details
            for i in range(len(points)-1):
                pygame.draw.line(self.surface, colors["primary"][1],
                               points[0], points[i+1], 1)
        
        # Body
        body_size = int(self.size * ratios["body"])
        pygame.draw.rect(self.surface, colors["primary"][0],
                        (self.size//2 - body_size//2, self.size//3, 
                         body_size, body_size))
        
        # Head
        head_size = int(self.size * ratios["head"])
        head_points = [
            (self.size//2 - head_size//2, self.size//3),  # Back
            (self.size//2 + head_size//2, self.size//3 - head_size//2),  # Top
            (self.size//2 + head_size, self.size//3),  # Snout
        ]
        pygame.draw.polygon(self.surface, colors["primary"][0], head_points)
        
        # Eyes (glowing)
        eye_size = head_size//4
        eye_pos = (self.size//2 + head_size//4, self.size//3 - head_size//4)
        pygame.draw.circle(self.surface, (*colors["secondary"][0][:3], 100),
                         eye_pos, eye_size)  # Glow
        pygame.draw.circle(self.surface, colors["secondary"][0],
                         eye_pos, eye_size//2)  # Core
            
    def _draw_necromancer(self, config, colors):
        """Draw necromancer with dark magic effects"""
        parts = config["parts"]
        ratios = config["size_ratio"]
        
        # Cloak
        cloak_size = int(self.size * ratios["cloak"])
        points = [
            (self.size//2, self.size//4),  # Top
            (self.size//4, self.size//2),  # Left shoulder
            (self.size*3//4, self.size//2),  # Right shoulder
            (self.size*3//4 + cloak_size//4, self.size*3//4),  # Bottom right
            (self.size//4 - cloak_size//4, self.size*3//4),  # Bottom left
        ]
        pygame.draw.polygon(self.surface, colors["primary"][0], points)
        
        # Body
        body_size = int(self.size * ratios["body"])
        pygame.draw.rect(self.surface, colors["primary"][1],
                        (self.size//2 - body_size//2, self.size//3,
                         body_size, body_size))
        
        # Staff
        staff_length = int(self.size * ratios["staff"])
        staff_start = (self.size*3//4, self.size//2)
        staff_end = (staff_start[0], staff_start[1] - staff_length)
        pygame.draw.line(self.surface, colors["secondary"][0],
                        staff_start, staff_end, 2)
        
        # Staff crystal
        crystal_pos = staff_end
        # Glow
        pygame.draw.circle(self.surface, (*colors["secondary"][0][:3], 100),
                         crystal_pos, 6)
        # Core
        pygame.draw.circle(self.surface, colors["secondary"][0],
                         crystal_pos, 4)
        
        # Dark magic particles
        for _ in range(3):
            x = random.randint(self.size//3, 2*self.size//3)
            y = random.randint(self.size//3, 2*self.size//3)
            pygame.draw.circle(self.surface, colors["secondary"][0],
                             (x, y), 2)
            
    def _draw_vampire(self, config, colors):
        """Draw vampire with elegant and sinister features"""
        parts = config["parts"]
        ratios = config["size_ratio"]
        
        # Cape
        cape_size = int(self.size * ratios["cape"])
        cape_points = [
            (self.size//2, self.size//4),  # Top
            (self.size//4, self.size//2),  # Left shoulder
            (self.size*3//4, self.size//2),  # Right shoulder
            (self.size*3//4 + cape_size//3, self.size*3//4),  # Bottom right
            (self.size//4 - cape_size//3, self.size*3//4),  # Bottom left
        ]
        pygame.draw.polygon(self.surface, colors["primary"][0], cape_points)
        
        # Body
        body_size = int(self.size * ratios["body"])
        pygame.draw.rect(self.surface, colors["primary"][1],
                        (self.size//2 - body_size//2, self.size//3,
                         body_size, body_size))
        
        # Head
        head_size = int(self.size * ratios["head"])
        pygame.draw.rect(self.surface, colors["primary"][0],
                        (self.size//2 - head_size//2, self.size//4,
                         head_size, head_size))
        
        # Eyes (glowing red)
        eye_size = 2
        eye_y = self.size//4 + head_size//2
        for x_offset in [-3, 3]:
            eye_x = self.size//2 + x_offset
            # Glow
            pygame.draw.circle(self.surface, (*colors["secondary"][0][:3], 100),
                             (eye_x, eye_y), eye_size + 1)
            # Core
            pygame.draw.circle(self.surface, colors["secondary"][0],
                             (eye_x, eye_y), eye_size)
            
    def _draw_demon_lord(self, config, colors):
        """Draw demon lord with imposing features"""
        parts = config["parts"]
        ratios = config["size_ratio"]
        
        # Wings
        wing_size = int(self.size * ratios["wings"])
        for x_offset in [-1, 1]:
            points = [
                (self.size//2, self.size//2),  # Base
                (self.size//2 + x_offset * wing_size, self.size//4),  # Top
                (self.size//2 + x_offset * wing_size * 1.2, self.size//2),  # Middle
                (self.size//2 + x_offset * wing_size, self.size*3//4),  # Bottom
            ]
            pygame.draw.polygon(self.surface, colors["primary"][0], points)
            
            # Wing details (fire veins)
            for i in range(len(points)-1):
                pygame.draw.line(self.surface, colors["secondary"][0],
                               points[0], points[i+1], 1)
        
        # Body
        body_size = int(self.size * ratios["body"])
        pygame.draw.rect(self.surface, colors["primary"][0],
                        (self.size//2 - body_size//2, self.size//3,
                         body_size, body_size))
        
        # Horns
        horn_size = int(self.size * ratios["horns"])
        for x_offset in [-1, 1]:
            points = [
                (self.size//2 + x_offset * body_size//3, self.size//3),  # Base
                (self.size//2 + x_offset * (body_size//3 + horn_size), self.size//4),  # Tip
                (self.size//2 + x_offset * (body_size//3 + horn_size//2), self.size//3),  # Back
            ]
            pygame.draw.polygon(self.surface, colors["primary"][1], points)
        
        # Crown
        crown_size = int(self.size * ratios["crown"])
        crown_points = []
        for i in range(5):
            x = self.size//2 - crown_size + i * crown_size//2
            y = self.size//3 - (i % 2) * crown_size//2
            crown_points.append((x, y))
        pygame.draw.polygon(self.surface, colors["secondary"][1], crown_points)
        
        # Eyes (intense glow)
        eye_size = body_size//5
        for x_offset in [-1, 1]:
            eye_pos = (self.size//2 + x_offset * body_size//3,
                      self.size//2)
            # Outer glow
            pygame.draw.circle(self.surface, (*colors["secondary"][0][:3], 100),
                             eye_pos, eye_size)
            # Inner glow
            pygame.draw.circle(self.surface, colors["secondary"][0],
                             eye_pos, eye_size//2)
            
    def _draw_lich(self, config, colors):
        """Draw lich with arcane power"""
        parts = config["parts"]
        ratios = config["size_ratio"]
        
        # Robe
        robe_size = int(self.size * ratios["robe"])
        robe_points = [
            (self.size//2, self.size//4),  # Top
            (self.size//3, self.size//2),  # Left shoulder
            (self.size*2//3, self.size//2),  # Right shoulder
            (self.size*2//3 + robe_size//4, self.size*3//4),  # Bottom right
            (self.size//3 - robe_size//4, self.size*3//4),  # Bottom left
        ]
        pygame.draw.polygon(self.surface, colors["primary"][0], robe_points)
        
        # Body
        body_size = int(self.size * ratios["body"])
        pygame.draw.rect(self.surface, colors["primary"][1],
                        (self.size//2 - body_size//2, self.size//3,
                         body_size, body_size))
        
        # Crown
        crown_size = int(self.size * ratios["crown"])
        crown_points = []
        for i in range(5):
            x = self.size//2 - crown_size + i * crown_size//2
            y = self.size//4 - (i % 2) * crown_size//2
            crown_points.append((x, y))
        pygame.draw.polygon(self.surface, colors["secondary"][0], crown_points)
        
        # Staff
        staff_length = int(self.size * ratios["staff"])
        staff_start = (self.size*2//3, self.size//2)
        staff_end = (staff_start[0], staff_start[1] - staff_length)
        pygame.draw.line(self.surface, colors["secondary"][0],
                        staff_start, staff_end, 2)
        
        # Staff orb (phylactery)
        orb_pos = staff_end
        # Outer glow
        pygame.draw.circle(self.surface, (*colors["secondary"][0][:3], 100),
                         orb_pos, 8)
        # Inner orb
        pygame.draw.circle(self.surface, colors["secondary"][0],
                         orb_pos, 5)
        
        # Arcane runes
        for _ in range(5):
            x = random.randint(self.size//3, 2*self.size//3)
            y = random.randint(self.size//3, 2*self.size//3)
            self._draw_rune(x, y, colors["secondary"][0]) 