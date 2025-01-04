import pygame
import random
import math

class WeaponAnimation:
    def __init__(self, frames, frame_duration):
        self.frames = frames  # List of functions that generate each frame
        self.current_frame = 0
        self.frame_duration = frame_duration
        self.frame_timer = 0
        self.is_playing = False
        
    def play(self):
        self.is_playing = True
        self.current_frame = 0
        self.frame_timer = 0
        
    def update(self):
        if not self.is_playing:
            return
            
        self.frame_timer += 1
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.current_frame = 0
                self.is_playing = False
                
    def draw(self, surface, x, y, angle):
        if not self.frames:
            return
        self.frames[self.current_frame](surface, x, y, angle)

class EquipmentSprites:
    def __init__(self, size):
        self.size = size
        # Define color palettes for different materials
        self.colors = {
            'metal': [(192, 192, 192), (160, 160, 160), (128, 128, 128)],  # Silver tones
            'gold': [(255, 215, 0), (218, 165, 32), (184, 134, 11)],      # Gold tones
            'cloth': [(255, 255, 255), (240, 240, 240), (220, 220, 220)], # White cloth
            'leather': [(139, 69, 19), (160, 82, 45), (210, 105, 30)],    # Brown leather
            'magic': [(148, 0, 211), (138, 43, 226), (147, 112, 219)]     # Purple magic
        }
        
        # Initialize weapon animations dictionary
        self.animations = {}
        self._setup_animations()
        
    def _setup_animations(self):
        # Knife animation
        knife_frames = [
            lambda s, x, y, a: self._draw_knife_frame(s, x, y, a, 0),  # Start position
            lambda s, x, y, a: self._draw_knife_frame(s, x, y, a, 1),  # Mid swing
            lambda s, x, y, a: self._draw_knife_frame(s, x, y, a, 2),  # Full extension
            lambda s, x, y, a: self._draw_knife_frame(s, x, y, a, 1),  # Return swing
        ]
        self.animations["Knife"] = WeaponAnimation(knife_frames, 3)
        
        # Whip animation
        whip_frames = [
            lambda s, x, y, a: self._draw_whip_frame(s, x, y, a, 0),  # Coiled
            lambda s, x, y, a: self._draw_whip_frame(s, x, y, a, 1),  # Extending
            lambda s, x, y, a: self._draw_whip_frame(s, x, y, a, 2),  # Full extension
            lambda s, x, y, a: self._draw_whip_frame(s, x, y, a, 1),  # Retracting
        ]
        self.animations["Whip"] = WeaponAnimation(whip_frames, 3)
        
        # Magic Wand animation
        wand_frames = [
            lambda s, x, y, a: self._draw_magic_wand_frame(s, x, y, a, 0),  # Normal
            lambda s, x, y, a: self._draw_magic_wand_frame(s, x, y, a, 1),  # Glowing
            lambda s, x, y, a: self._draw_magic_wand_frame(s, x, y, a, 2),  # Bright
            lambda s, x, y, a: self._draw_magic_wand_frame(s, x, y, a, 1),  # Fading
        ]
        self.animations["Magic Wand"] = WeaponAnimation(wand_frames, 4)
        
        # Fire Wand animation
        fire_frames = [
            lambda s, x, y, a: self._draw_fire_wand_frame(s, x, y, a, 0),  # Normal
            lambda s, x, y, a: self._draw_fire_wand_frame(s, x, y, a, 1),  # Heating
            lambda s, x, y, a: self._draw_fire_wand_frame(s, x, y, a, 2),  # Burning
            lambda s, x, y, a: self._draw_fire_wand_frame(s, x, y, a, 1),  # Cooling
        ]
        self.animations["Fire Wand"] = WeaponAnimation(fire_frames, 4)

        # CrossBow animation
        crossbow_frames = [
            lambda s, x, y, a: self._draw_crossbow_frame(s, x, y, a, 0),  # Ready
            lambda s, x, y, a: self._draw_crossbow_frame(s, x, y, a, 1),  # Firing
            lambda s, x, y, a: self._draw_crossbow_frame(s, x, y, a, 2),  # Recoil
            lambda s, x, y, a: self._draw_crossbow_frame(s, x, y, a, 1),  # Reloading
        ]
        self.animations["Cross Bow"] = WeaponAnimation(crossbow_frames, 3)

        # Lightning Ring animation
        lightning_frames = [
            lambda s, x, y, a: self._draw_lightning_ring_frame(s, x, y, a, 0),  # Charging
            lambda s, x, y, a: self._draw_lightning_ring_frame(s, x, y, a, 1),  # Sparking
            lambda s, x, y, a: self._draw_lightning_ring_frame(s, x, y, a, 2),  # Full discharge
            lambda s, x, y, a: self._draw_lightning_ring_frame(s, x, y, a, 1),  # Fading
        ]
        self.animations["Lightning Ring"] = WeaponAnimation(lightning_frames, 3)

    def _draw_knife_frame(self, surface, x, y, angle, frame):
        # Base knife shape
        knife_length = 20
        blade_width = 4
        
        # Adjust angle based on animation frame
        if frame == 0:  # Start position
            swing_offset = -30
        elif frame == 1:  # Mid swing
            swing_offset = 0
        else:  # Full extension
            swing_offset = 30
            
        total_angle = angle + swing_offset
        
        # Calculate points for knife shape
        rad_angle = math.radians(total_angle)
        tip_x = x + math.cos(rad_angle) * knife_length
        tip_y = y + math.sin(rad_angle) * knife_length
        
        # Draw blade
        pygame.draw.line(surface, (200, 200, 200), (x, y), (tip_x, tip_y), 3)
        
        # Draw handle
        handle_length = 8
        handle_x = x - math.cos(rad_angle) * handle_length
        handle_y = y - math.sin(rad_angle) * handle_length
        pygame.draw.line(surface, (139, 69, 19), (x, y), (handle_x, handle_y), 4)

    def _draw_whip_frame(self, surface, x, y, angle, frame):
        # Whip parameters
        segments = 8
        segment_length = 6
        
        # Calculate whip curve based on frame
        points = [(x, y)]
        
        for i in range(segments):
            if frame == 0:  # Coiled
                segment_angle = angle + (i * 30)
                dist = segment_length * 0.5
            elif frame == 1:  # Extending
                segment_angle = angle + (i * 20)
                dist = segment_length * 0.75
            elif frame == 2:  # Full extension
                segment_angle = angle + (i * 10)
                dist = segment_length
            else:  # Retracting
                segment_angle = angle + (i * 20)
                dist = segment_length * 0.75
                
            rad_angle = math.radians(segment_angle)
            next_x = points[-1][0] + math.cos(rad_angle) * dist
            next_y = points[-1][1] + math.sin(rad_angle) * dist
            points.append((next_x, next_y))
        
        # Draw whip segments
        for i in range(len(points) - 1):
            color = (139, 69, 19)  # Brown color
            width = max(1, 3 - (i // 2))  # Gradually thin out
            pygame.draw.line(surface, color, points[i], points[i + 1], width)

    def _draw_magic_wand_frame(self, surface, x, y, angle, frame):
        # Wand parameters
        wand_length = 20
        rad_angle = math.radians(angle)
        
        # Calculate wand end points
        end_x = x + math.cos(rad_angle) * wand_length
        end_y = y + math.sin(rad_angle) * wand_length
        
        # Draw wand body
        pygame.draw.line(surface, (139, 69, 19), (x, y), (end_x, end_y), 3)
        
        # Draw magical effect based on frame
        if frame > 0:
            glow_radius = 4 + frame * 2
            glow_color = (100, 200, 255, 150 - frame * 30)
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
            surface.blit(glow_surface, (end_x - glow_radius, end_y - glow_radius))
            
            # Add sparkles
            for _ in range(frame * 2):
                sparkle_angle = angle + random.uniform(-30, 30)
                sparkle_dist = random.uniform(5, 10)
                sparkle_x = end_x + math.cos(math.radians(sparkle_angle)) * sparkle_dist
                sparkle_y = end_y + math.sin(math.radians(sparkle_angle)) * sparkle_dist
                pygame.draw.circle(surface, (200, 255, 255), (int(sparkle_x), int(sparkle_y)), 1)

    def _draw_fire_wand_frame(self, surface, x, y, angle, frame):
        # Wand parameters
        wand_length = 20
        rad_angle = math.radians(angle)
        
        # Calculate wand end points
        end_x = x + math.cos(rad_angle) * wand_length
        end_y = y + math.sin(rad_angle) * wand_length
        
        # Draw wand body
        pygame.draw.line(surface, (139, 69, 19), (x, y), (end_x, end_y), 3)
        
        # Draw fire effect based on frame
        if frame > 0:
            for _ in range(3 + frame * 2):
                flame_angle = angle + random.uniform(-20, 20)
                flame_length = random.uniform(5, 10 + frame * 3)
                flame_x = end_x + math.cos(math.radians(flame_angle)) * flame_length
                flame_y = end_y + math.sin(math.radians(flame_angle)) * flame_length
                
                # Gradient from yellow to red
                color = (255, max(0, 255 - frame * 50), 0, 150)
                pygame.draw.line(surface, color, (end_x, end_y), (flame_x, flame_y), 2)

    def _draw_crossbow_frame(self, surface, x, y, angle, frame):
        # Base parameters
        rad_angle = math.radians(angle)
        bow_size = 15
        stock_length = 12
        
        # Calculate main points
        front_x = x + math.cos(rad_angle) * bow_size
        front_y = y + math.sin(rad_angle) * bow_size
        back_x = x - math.cos(rad_angle) * stock_length
        back_y = y - math.sin(rad_angle) * stock_length
        
        # Draw stock
        pygame.draw.line(surface, (139, 69, 19), (back_x, back_y), (x, y), 4)  # Wooden stock
        
        # Draw bow arms
        arm_angle = math.pi/4  # 45 degrees
        arm_length = 8
        
        # Left arm
        left_x = front_x + math.cos(rad_angle + arm_angle) * arm_length
        left_y = front_y + math.sin(rad_angle + arm_angle) * arm_length
        pygame.draw.line(surface, (200, 200, 200), (front_x, front_y), (left_x, left_y), 2)
        
        # Right arm
        right_x = front_x + math.cos(rad_angle - arm_angle) * arm_length
        right_y = front_y + math.sin(rad_angle - arm_angle) * arm_length
        pygame.draw.line(surface, (200, 200, 200), (front_x, front_y), (right_x, right_y), 2)
        
        # Draw string based on frame
        if frame == 0:  # Ready
            pygame.draw.line(surface, (255, 255, 255), (left_x, left_y), (right_x, right_y), 1)
        elif frame == 1:  # Firing
            # String is pulled back
            string_pull = 5
            string_x = x - math.cos(rad_angle) * string_pull
            string_y = y - math.sin(rad_angle) * string_pull
            pygame.draw.line(surface, (255, 255, 255), (left_x, left_y), (string_x, string_y), 1)
            pygame.draw.line(surface, (255, 255, 255), (string_x, string_y), (right_x, right_y), 1)
            
            # Draw bolt
            bolt_length = 10
            bolt_x = front_x + math.cos(rad_angle) * bolt_length
            bolt_y = front_y + math.sin(rad_angle) * bolt_length
            pygame.draw.line(surface, (150, 150, 150), (front_x, front_y), (bolt_x, bolt_y), 2)
        else:  # Recoil/reloading
            pygame.draw.line(surface, (255, 255, 255), (left_x, left_y), (right_x, right_y), 1)

    def _draw_lightning_ring_frame(self, surface, x, y, angle, frame):
        # Ring parameters
        ring_radius = 8
        
        # Draw base ring
        pygame.draw.circle(surface, (200, 200, 200), (int(x), int(y)), ring_radius, 2)
        
        # Draw lightning effects based on frame
        if frame > 0:
            num_bolts = 2 + frame  # More bolts in later frames
            for i in range(num_bolts):
                start_angle = angle + (i * 360 / num_bolts) + random.uniform(-20, 20)
                points = [(x, y)]
                
                # Create lightning bolt
                segments = 3
                for j in range(segments):
                    bolt_length = ring_radius + (frame * 5) + random.uniform(0, 5)
                    bolt_angle = math.radians(start_angle + random.uniform(-30, 30))
                    next_x = points[-1][0] + math.cos(bolt_angle) * bolt_length
                    next_y = points[-1][1] + math.sin(bolt_angle) * bolt_length
                    points.append((next_x, next_y))
                
                # Draw the lightning bolt
                alpha = min(255, 150 + frame * 50)
                color = (100, 150, 255, alpha)
                pygame.draw.lines(surface, color, False, points, 2)
                
                # Add glow effect
                if frame == 2:  # Full discharge frame
                    glow_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surface, (100, 150, 255, 50), (10, 10), 8)
                    surface.blit(glow_surface, (x - 10, y - 10))

    def generate_weapon_sprite(self, weapon_name):
        """Create a new surface for the weapon sprite"""
        surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        return surface  # Now just return empty surface as actual drawing happens in animation

    def get_animation(self, weapon_name):
        """Get the animation for a specific weapon"""
        return self.animations.get(weapon_name)

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