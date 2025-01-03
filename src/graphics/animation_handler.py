import pygame
import math

class AnimationHandler:
    def __init__(self, base_sprite):
        self.base_sprite = base_sprite
        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 6  # Frames per animation state
        
        # Create animation frames from base sprite
        self.animations = {
            'idle': self._generate_idle_frames(),
            'walk': self._generate_walk_frames(),
            'attack': self._generate_attack_frames()
        }
        self.current_animation = 'idle'
        
    def _generate_idle_frames(self):
        """Generate subtle breathing/floating animation frames"""
        frames = []
        sprite_size = self.base_sprite.get_width()
        
        for i in range(4):  # 4 frame animation
            frame = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            # Slight vertical movement for breathing effect
            offset = math.sin(i * math.pi/2) * 1  # 1 pixel up/down
            frame.blit(self.base_sprite, (0, offset))
            frames.append(frame)
            
        return frames
        
    def _generate_walk_frames(self):
        """Generate walking animation frames"""
        frames = []
        sprite_size = self.base_sprite.get_width()
        
        for i in range(4):  # 4 frame animation
            frame = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            # Bobbing motion
            vertical_offset = abs(math.sin(i * math.pi/2)) * 2
            # Slight tilt
            angle = math.sin(i * math.pi/2) * 5  # -5 to 5 degrees
            
            # Rotate and position sprite
            rotated = pygame.transform.rotate(self.base_sprite, angle)
            # Adjust position to keep centered
            x = (sprite_size - rotated.get_width()) // 2
            y = vertical_offset
            frame.blit(rotated, (x, y))
            frames.append(frame)
            
        return frames
        
    def _generate_attack_frames(self):
        """Generate attack animation frames"""
        frames = []
        sprite_size = self.base_sprite.get_width()
        
        # Frame 1: Wind up (slight back tilt)
        frame1 = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
        rotated1 = pygame.transform.rotate(self.base_sprite, 15)
        x1 = (sprite_size - rotated1.get_width()) // 2
        y1 = (sprite_size - rotated1.get_height()) // 2
        frame1.blit(rotated1, (x1, y1))
        frames.append(frame1)
        
        # Frame 2: Attack (forward tilt)
        frame2 = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
        rotated2 = pygame.transform.rotate(self.base_sprite, -20)
        x2 = (sprite_size - rotated2.get_width()) // 2
        y2 = (sprite_size - rotated2.get_height()) // 2
        frame2.blit(rotated2, (x2, y2))
        frames.append(frame2)
        
        # Frame 3: Follow through
        frame3 = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
        rotated3 = pygame.transform.rotate(self.base_sprite, -10)
        x3 = (sprite_size - rotated3.get_width()) // 2
        y3 = (sprite_size - rotated3.get_height()) // 2
        frame3.blit(rotated3, (x3, y3))
        frames.append(frame3)
        
        # Frame 4: Return to neutral
        frames.append(self.base_sprite.copy())
        
        return frames
        
    def update(self):
        """Update animation state"""
        self.animation_timer += 1
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            
    def set_animation(self, animation_name):
        """Change current animation"""
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.current_frame = 0
            self.animation_timer = 0
            
    def get_current_frame(self):
        """Get the current animation frame"""
        return self.animations[self.current_animation][self.current_frame] 