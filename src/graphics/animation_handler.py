import pygame
import math
import random

class AnimationHandler:
    def __init__(self, base_sprite):
        self.base_sprite = base_sprite
        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 6  # Frames per animation state
        self.movement_bob = 0
        self.dust_particles = []
        
        # Create animation frames from base sprite
        self.animations = {
            'idle': self._generate_idle_frames(),
            'walk': self._generate_walk_frames(),
            'attack': self._generate_attack_frames(),
            'dash': self._generate_dash_frames(),
            'hurt': self._generate_hurt_frames()
        }
        self.current_animation = 'idle'
        
    def _generate_idle_frames(self):
        """Generate improved breathing/floating animation frames"""
        frames = []
        sprite_size = self.base_sprite.get_width()
        
        for i in range(6):  # Increased to 6 frames for smoother animation
            frame = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            # Combine vertical and slight horizontal movement
            offset_y = math.sin(i * math.pi/3) * 1.5
            offset_x = math.cos(i * math.pi/3) * 0.5
            # Add subtle scaling effect
            scale = 1.0 + math.sin(i * math.pi/3) * 0.02
            scaled = pygame.transform.scale(
                self.base_sprite,
                (int(sprite_size * scale), int(sprite_size * scale))
            )
            # Center the scaled sprite
            x = (sprite_size - scaled.get_width()) // 2 + offset_x
            y = (sprite_size - scaled.get_height()) // 2 + offset_y
            frame.blit(scaled, (x, y))
            frames.append(frame)
            
        return frames
        
    def _generate_walk_frames(self):
        """Generate improved walking animation frames"""
        frames = []
        sprite_size = self.base_sprite.get_width()
        
        for i in range(8):  # Increased to 8 frames for smoother animation
            frame = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            # Enhanced bobbing motion
            vertical_offset = math.sin(i * math.pi/4) * 3
            # Dynamic tilt based on movement
            tilt = math.sin(i * math.pi/4) * 8
            # Add squash and stretch
            stretch = 1.0 + abs(math.sin(i * math.pi/4)) * 0.1
            squeeze = 1.0 - abs(math.sin(i * math.pi/4)) * 0.1
            
            # Scale sprite with squash and stretch
            scaled = pygame.transform.scale(
                self.base_sprite,
                (int(sprite_size * squeeze), int(sprite_size * stretch))
            )
            # Rotate scaled sprite
            rotated = pygame.transform.rotate(scaled, tilt)
            
            # Position with offset
            x = (sprite_size - rotated.get_width()) // 2
            y = (sprite_size - rotated.get_height()) // 2 + vertical_offset
            frame.blit(rotated, (x, y))
            frames.append(frame)
            
        return frames
        
    def _generate_attack_frames(self):
        """Generate improved attack animation frames"""
        frames = []
        sprite_size = self.base_sprite.get_width()
        
        # Frame 1: Wind up (anticipation)
        frame1 = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
        scaled1 = pygame.transform.scale(self.base_sprite, 
                                      (int(sprite_size * 1.1), int(sprite_size * 0.9)))
        rotated1 = pygame.transform.rotate(scaled1, 15)
        x1 = (sprite_size - rotated1.get_width()) // 2 - 2
        y1 = (sprite_size - rotated1.get_height()) // 2
        frame1.blit(rotated1, (x1, y1))
        frames.append(frame1)
        
        # Frame 2: Attack (stretch)
        frame2 = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
        scaled2 = pygame.transform.scale(self.base_sprite, 
                                      (int(sprite_size * 1.2), int(sprite_size * 0.8)))
        rotated2 = pygame.transform.rotate(scaled2, -20)
        x2 = (sprite_size - rotated2.get_width()) // 2 + 4
        y2 = (sprite_size - rotated2.get_height()) // 2
        frame2.blit(rotated2, (x2, y2))
        frames.append(frame2)
        
        # Frame 3: Impact
        frame3 = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
        scaled3 = pygame.transform.scale(self.base_sprite, 
                                      (int(sprite_size * 1.15), int(sprite_size * 0.85)))
        rotated3 = pygame.transform.rotate(scaled3, -10)
        x3 = (sprite_size - rotated3.get_width()) // 2 + 2
        y3 = (sprite_size - rotated3.get_height()) // 2
        frame3.blit(rotated3, (x3, y3))
        frames.append(frame3)
        
        # Frame 4: Recovery
        frame4 = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
        scaled4 = pygame.transform.scale(self.base_sprite, 
                                      (int(sprite_size * 1.05), int(sprite_size * 0.95)))
        x4 = (sprite_size - scaled4.get_width()) // 2
        y4 = (sprite_size - scaled4.get_height()) // 2
        frame4.blit(scaled4, (x4, y4))
        frames.append(frame4)
        
        return frames
        
    def _generate_dash_frames(self):
        """Generate dash animation frames"""
        frames = []
        sprite_size = self.base_sprite.get_width()
        
        for i in range(4):
            frame = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            # Horizontal stretch effect
            stretch = 1.3 - (i / 4) * 0.3
            squeeze = 0.7 + (i / 4) * 0.3
            
            scaled = pygame.transform.scale(
                self.base_sprite,
                (int(sprite_size * stretch), int(sprite_size * squeeze))
            )
            
            x = (sprite_size - scaled.get_width()) // 2
            y = (sprite_size - scaled.get_height()) // 2
            frame.blit(scaled, (x, y))
            frames.append(frame)
            
        return frames
        
    def _generate_hurt_frames(self):
        """Generate hurt animation frames"""
        frames = []
        sprite_size = self.base_sprite.get_width()
        
        for i in range(4):
            frame = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            # Flash red and shake
            red_tint = self.base_sprite.copy()
            red_tint.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Random shake offset
            shake_x = random.randint(-2, 2)
            shake_y = random.randint(-2, 2)
            
            frame.blit(red_tint, (shake_x, shake_y))
            frames.append(frame)
            
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

class GunAnimationHandler:
    def __init__(self, gun_sprite):
        self.gun_sprite = gun_sprite
        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 4  # Faster than character animations
        self.recoil_offset = 0
        self.muzzle_flash_alpha = 0
        
        # Create animation frames
        self.animations = {
            'idle': self._generate_idle_frames(),
            'shoot': self._generate_shoot_frames(),
            'reload': self._generate_reload_frames()
        }
        self.current_animation = 'idle'
        
    def _generate_idle_frames(self):
        """Generate subtle floating animation for gun"""
        frames = []
        sprite_size = self.gun_sprite.get_width()
        
        for i in range(4):
            frame = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            # Subtle hovering effect
            offset_y = math.sin(i * math.pi/2) * 1
            offset_x = math.cos(i * math.pi/2) * 0.5
            frame.blit(self.gun_sprite, (offset_x, offset_y))
            frames.append(frame)
            
        return frames
        
    def _generate_shoot_frames(self):
        """Generate shooting animation with recoil"""
        frames = []
        sprite_size = self.gun_sprite.get_width()
        
        # Frame 1: Recoil back
        frame1 = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
        rotated1 = pygame.transform.rotate(self.gun_sprite, 15)  # Kick up
        frame1.blit(rotated1, (-4, 0))  # Recoil back
        frames.append(frame1)
        
        # Frame 2: Maximum recoil
        frame2 = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
        rotated2 = pygame.transform.rotate(self.gun_sprite, 20)
        frame2.blit(rotated2, (-6, 0))
        frames.append(frame2)
        
        # Frame 3: Recovery
        frame3 = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
        rotated3 = pygame.transform.rotate(self.gun_sprite, 10)
        frame3.blit(rotated3, (-2, 0))
        frames.append(frame3)
        
        # Frame 4: Return to position
        frame4 = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
        frame4.blit(self.gun_sprite, (0, 0))
        frames.append(frame4)
        
        return frames
        
    def _generate_reload_frames(self):
        """Generate reload animation"""
        frames = []
        sprite_size = self.gun_sprite.get_width()
        
        for i in range(6):  # 6 frame animation
            frame = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            # Spin effect
            angle = i * 60  # 360 degrees / 6 frames
            rotated = pygame.transform.rotate(self.gun_sprite, angle)
            # Keep centered during rotation
            x = (sprite_size - rotated.get_width()) // 2
            y = (sprite_size - rotated.get_height()) // 2
            frame.blit(rotated, (x, y))
            frames.append(frame)
            
        return frames
        
    def update(self):
        """Update animation state"""
        self.animation_timer += 1
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            
            # Reset to idle after shoot animation completes
            if self.current_animation == 'shoot' and self.current_frame == 0:
                self.current_animation = 'idle'
                
        # Update muzzle flash
        if self.muzzle_flash_alpha > 0:
            self.muzzle_flash_alpha = max(0, self.muzzle_flash_alpha - 25)
            
    def set_animation(self, animation_name):
        """Change current animation"""
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.current_frame = 0
            self.animation_timer = 0
            
            # Add muzzle flash when shooting
            if animation_name == 'shoot':
                self.muzzle_flash_alpha = 255
            
    def get_current_frame(self):
        """Get the current animation frame"""
        return self.animations[self.current_animation][self.current_frame]
        
    def get_muzzle_flash(self):
        """Get muzzle flash surface if active"""
        if self.muzzle_flash_alpha <= 0:
            return None
            
        flash = pygame.Surface((20, 20), pygame.SRCALPHA)
        color = (*YELLOW, self.muzzle_flash_alpha)
        pygame.draw.circle(flash, color, (10, 10), 10)
        return flash 