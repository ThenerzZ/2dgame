import pygame
import math
import random
from enum import Enum

class EaseType(Enum):
    LINEAR = 0
    EASE_IN = 1
    EASE_OUT = 2
    EASE_IN_OUT = 3
    BOUNCE = 4
    ELASTIC = 5

class AnimationState:
    def __init__(self, name, frames, duration, loop=True, next_state=None, ease_type=EaseType.LINEAR):
        self.name = name
        self.frames = frames
        self.duration = duration
        self.loop = loop
        self.next_state = next_state
        self.ease_type = ease_type
        self.frame_count = len(frames)
        
    def get_progress(self, time):
        """Get animation progress with easing applied"""
        progress = (time % self.duration) / self.duration if self.loop else min(time / self.duration, 1)
        
        if self.ease_type == EaseType.LINEAR:
            return progress
        elif self.ease_type == EaseType.EASE_IN:
            return progress * progress
        elif self.ease_type == EaseType.EASE_OUT:
            return 1 - (1 - progress) * (1 - progress)
        elif self.ease_type == EaseType.EASE_IN_OUT:
            if progress < 0.5:
                return 2 * progress * progress
            else:
                return 1 - (-2 * progress + 2) ** 2 / 2
        elif self.ease_type == EaseType.BOUNCE:
            if progress < 1 / 2.75:
                return 7.5625 * progress * progress
            elif progress < 2 / 2.75:
                progress -= 1.5 / 2.75
                return 7.5625 * progress * progress + 0.75
            elif progress < 2.5 / 2.75:
                progress -= 2.25 / 2.75
                return 7.5625 * progress * progress + 0.9375
            else:
                progress -= 2.625 / 2.75
                return 7.5625 * progress * progress + 0.984375
        elif self.ease_type == EaseType.ELASTIC:
            if progress == 0 or progress == 1:
                return progress
            progress = progress * 2
            if progress < 1:
                return -0.5 * (math.pow(2, 10 * (progress - 1)) * math.sin((progress - 1.1) * 5 * math.pi))
            return 0.5 * math.pow(2, -10 * (progress - 1)) * math.sin((progress - 1.1) * 5 * math.pi) + 1

class AnimationHandler:
    def __init__(self, base_sprite):
        self.base_sprite = base_sprite
        self.sprite_size = base_sprite.get_width()
        self.current_time = 0
        self.animation_states = self._create_animation_states()
        self.current_state = self.animation_states['idle']
        self.transition_time = 0
        self.transition_duration = 5
        self.prev_frame = self.current_state.frames[0].copy()
        self.next_frame = None
        
    def _create_animation_states(self):
        return {
            'idle': AnimationState('idle', self._generate_idle_frames(), 60, True, None, EaseType.EASE_IN_OUT),
            'walk': AnimationState('walk', self._generate_walk_frames(), 48, True, None, EaseType.EASE_IN_OUT),
            'attack': AnimationState('attack', self._generate_attack_frames(), 30, False, 'idle', EaseType.EASE_OUT),
            'dash': AnimationState('dash', self._generate_dash_frames(), 20, False, 'idle', EaseType.EASE_OUT),
            'hurt': AnimationState('hurt', self._generate_hurt_frames(), 20, False, 'idle', EaseType.BOUNCE)
        }

    def _interpolate_frames(self, frame1, frame2, progress):
        """Simple frame crossfade without using special blend modes"""
        if progress <= 0:
            return frame1.copy()
        if progress >= 1:
            return frame2.copy()
            
        # Create a new surface for the interpolated frame
        result = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
        
        # Draw first frame with fading opacity
        frame1_copy = frame1.copy()
        frame1_copy.set_alpha(int((1 - progress) * 255))
        result.blit(frame1_copy, (0, 0))
        
        # Draw second frame with increasing opacity
        frame2_copy = frame2.copy()
        frame2_copy.set_alpha(int(progress * 255))
        result.blit(frame2_copy, (0, 0))
        
        return result

    def _generate_idle_frames(self):
        frames = []
        
        for i in range(8):  # Increased frame count for smoother animation
            frame = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
            progress = i / 7  # Normalized progress
            
            # Smooth breathing motion
            breath = math.sin(progress * 2 * math.pi)
            scale_y = 1.0 + breath * 0.02  # Subtle vertical scaling
            scale_x = 1.0 - breath * 0.01  # Slight horizontal compensation
            
            # Apply smooth scaling
            scaled = pygame.transform.scale(
                self.base_sprite,
                (int(self.sprite_size * scale_x), int(self.sprite_size * scale_y))
            )
            
            # Center the sprite
            x = (self.sprite_size - scaled.get_width()) // 2
            y = (self.sprite_size - scaled.get_height()) // 2 + breath * 0.5
            
            frame.blit(scaled, (x, y))
            frames.append(frame)
            
        return frames

    def _generate_walk_frames(self):
        frames = []
        
        for i in range(8):
            frame = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
            progress = i / 7
            
            # Smooth walking cycle
            cycle = math.sin(progress * 2 * math.pi)
            bounce = abs(math.sin(progress * math.pi * 2))
            
            # Dynamic scaling based on walk cycle
            scale_y = 1.0 + bounce * 0.04  # Vertical stretch during step
            scale_x = 1.0 - bounce * 0.02  # Slight horizontal squeeze
            
            # Forward lean
            lean = 3 + cycle * 2  # 3 degrees base lean + 2 degrees variation
            
            # Scale and rotate
            scaled = pygame.transform.scale(
                self.base_sprite,
                (int(self.sprite_size * scale_x), int(self.sprite_size * scale_y))
            )
            rotated = pygame.transform.rotate(scaled, lean)
            
            # Position with smooth bobbing
            x = (self.sprite_size - rotated.get_width()) // 2
            y = (self.sprite_size - rotated.get_height()) // 2 + bounce * 1.5
            
            frame.blit(rotated, (x, y))
            frames.append(frame)
            
        return frames

    def _generate_attack_frames(self):
        frames = []
        keyframes = [
            # (scale_x, scale_y, rotation, x_offset, y_offset)
            (0.98, 1.02, 3, -1, 0),    # Anticipation
            (1.1, 0.95, -10, 2, 0),    # Wind-up
            (1.15, 0.9, -15, 3, 1),    # Attack
            (1.05, 0.98, -8, 2, 0),    # Follow through
            (1.0, 1.0, 0, 0, 0)        # Recovery
        ]
        
        for i in range(5):
            frame = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
            scale_x, scale_y, rot, off_x, off_y = keyframes[i]
            
            # Apply transformations
            scaled = pygame.transform.scale(
                self.base_sprite,
                (int(self.sprite_size * scale_x), int(self.sprite_size * scale_y))
            )
            rotated = pygame.transform.rotate(scaled, rot)
            
            # Position frame
            x = (self.sprite_size - rotated.get_width()) // 2 + off_x
            y = (self.sprite_size - rotated.get_height()) // 2 + off_y
            
            frame.blit(rotated, (x, y))
            frames.append(frame)
            
        return frames

    def _generate_dash_frames(self):
        frames = []
        keyframes = [
            # (scale_x, scale_y, rotation, x_offset)
            (1.2, 0.9, -12, 3),    # Initial burst
            (1.3, 0.8, -15, 4),    # Maximum stretch
            (1.25, 0.85, -10, 3),  # Maintain speed
            (1.1, 0.95, -5, 2),    # Recovery
        ]
        
        for scale_x, scale_y, rot, off_x in keyframes:
            frame = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
            
            # Apply motion blur effect
            blur_steps = 3
            for j in range(blur_steps):
                alpha = 128 if j == 0 else 64 // (j + 1)
                blur_x = off_x * (j / blur_steps)
                
                temp = self.base_sprite.copy()
                temp.set_alpha(alpha)
                
                # Scale and rotate
                scaled = pygame.transform.scale(
                    temp,
                    (int(self.sprite_size * scale_x), int(self.sprite_size * scale_y))
                )
                rotated = pygame.transform.rotate(scaled, rot)
                
                # Position with blur offset
                x = (self.sprite_size - rotated.get_width()) // 2 + blur_x
                y = (self.sprite_size - rotated.get_height()) // 2
                
                frame.blit(rotated, (x, y))
            
            frames.append(frame)
            
        return frames

    def _generate_hurt_frames(self):
        frames = []
        
        for i in range(4):
            frame = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
            progress = i / 3
            
            # Flash effect
            flash_intensity = max(0, 1 - progress * 1.5)
            red_tint = self.base_sprite.copy()
            red_tint.fill((255, 0, 0, int(150 * flash_intensity)), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Impact deformation
            if i == 0:
                scale_x, scale_y = 1.2, 0.8  # Initial impact
            elif i == 1:
                scale_x, scale_y = 0.9, 1.1  # Rebound
            elif i == 2:
                scale_x, scale_y = 1.1, 0.9  # Secondary impact
            else:
                scale_x, scale_y = 1.0, 1.0  # Recovery
                
            # Apply scaling
            scaled = pygame.transform.scale(
                red_tint,
                (int(self.sprite_size * scale_x), int(self.sprite_size * scale_y))
            )
            
            # Add shake effect
            shake_amount = int((1 - progress) * 4)
            shake_x = random.randint(-shake_amount, shake_amount)
            shake_y = random.randint(-shake_amount, shake_amount)
            
            # Position with shake
            x = (self.sprite_size - scaled.get_width()) // 2 + shake_x
            y = (self.sprite_size - scaled.get_height()) // 2 + shake_y
            
            frame.blit(scaled, (x, y))
            frames.append(frame)
            
        return frames

    def update(self):
        """Update animation state"""
        self.current_time += 1
        
        # Check for state transition
        if not self.current_state.loop:
            progress = self.current_time / self.current_state.duration
            if progress >= 1 and self.current_state.next_state:
                self.set_animation(self.current_state.next_state)

    def set_animation(self, animation_name):
        """Change animation state with smooth transition"""
        if animation_name != self.current_state.name:
            self.prev_frame = self.get_current_frame()
            self.current_state = self.animation_states[animation_name]
            self.current_time = 0
            self.transition_time = self.transition_duration

    def get_current_frame(self):
        """Get current animation frame with interpolation"""
        # Normal animation playback
        progress = self.current_state.get_progress(self.current_time)
        frame_index = int(progress * (self.current_state.frame_count - 1))
        
        # Get the current frame
        current_frame = self.current_state.frames[frame_index]
        
        # Handle transition between states
        if self.transition_time > 0:
            transition_progress = 1 - (self.transition_time / self.transition_duration)
            self.transition_time -= 1
            
            # Interpolate between previous and current frame
            if self.prev_frame is not None:
                return self._interpolate_frames(self.prev_frame, current_frame, transition_progress)
        
        return current_frame.copy()  # Return a copy to prevent modification of original 