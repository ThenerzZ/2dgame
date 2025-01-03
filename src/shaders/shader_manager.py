import pygame
import numpy as np
from game.settings import *

class ShaderManager:
    def __init__(self):
        self.enabled = SHADER_ENABLED
        self.post_processing = POST_PROCESSING
        self.screen_surface = None
        self.temp_surface = None
        
    def initialize(self, screen_size):
        """Initialize shader surfaces"""
        if self.enabled:
            self.screen_surface = pygame.Surface(screen_size)
            self.temp_surface = pygame.Surface(screen_size)
            
    def apply_bloom(self, surface, intensity=1.5):
        """Apply bloom effect"""
        if not self.enabled or not self.post_processing:
            return surface
            
        # Create a blurred version of the surface
        self.temp_surface.blit(surface, (0, 0))
        pygame.transform.gaussian_blur(self.temp_surface, 3)
        
        # Blend the original and blurred surfaces
        surface.blit(self.temp_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        return surface
        
    def apply_color_grading(self, surface, tint_color=(1, 1, 1)):
        """Apply color grading"""
        if not self.enabled or not self.post_processing:
            return surface
            
        pixel_array = pygame.surfarray.pixels3d(surface)
        pixel_array = pixel_array * np.array(tint_color, dtype=np.uint8)
        del pixel_array  # Release the surface lock
        
        return surface
        
    def apply_vignette(self, surface, intensity=0.3):
        """Apply vignette effect"""
        if not self.enabled or not self.post_processing:
            return surface
            
        width, height = surface.get_size()
        self.temp_surface.fill((0, 0, 0))
        
        # Create radial gradient
        for x in range(width):
            for y in range(height):
                distance = np.sqrt((x - width/2)**2 + (y - height/2)**2)
                alpha = int(255 * (1 - (distance / (width/2)) * intensity))
                alpha = max(0, min(255, alpha))
                self.temp_surface.set_at((x, y), (0, 0, 0, alpha))
                
        surface.blit(self.temp_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return surface
        
    def apply_all_effects(self, surface):
        """Apply all post-processing effects"""
        if not self.enabled or not self.post_processing:
            return surface
            
        surface = self.apply_bloom(surface)
        surface = self.apply_color_grading(surface)
        surface = self.apply_vignette(surface)
        return surface 