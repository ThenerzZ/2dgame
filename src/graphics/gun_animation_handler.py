import pygame
import math
from game.settings import *

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