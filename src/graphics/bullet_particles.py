import pygame
import random
import math

class Bullet:
    def __init__(self, x, y, target_x, target_y, speed=10):
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        
        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx * dx + dy * dy)
        self.dx = (dx / distance) * speed if distance > 0 else 0
        self.dy = (dy / distance) * speed if distance > 0 else 0
        
        # Trail effect
        self.trail = []
        self.trail_length = 5
        self.dead = False
        self.lifetime = 60  # 1 second at 60 FPS
        
        # Bullet color with slight randomization
        base_color = (255, 200, 50)  # Golden yellow
        variation = random.randint(-20, 20)
        self.color = tuple(max(0, min(255, c + variation)) for c in base_color)

    def update(self):
        # Update position
        self.x += self.dx
        self.y += self.dy
        
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
            
        # Update lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.dead = True

    def draw(self, surface):
        # Draw trail
        if len(self.trail) > 1:
            # Calculate alpha for each trail segment
            for i in range(len(self.trail) - 1):
                alpha = int(255 * (i + 1) / len(self.trail))
                color = (*self.color, alpha)
                start_pos = (int(self.trail[i][0]), int(self.trail[i][1]))
                end_pos = (int(self.trail[i + 1][0]), int(self.trail[i + 1][1]))
                pygame.draw.line(surface, color, start_pos, end_pos, 2)
        
        # Draw bullet
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 2)

class MuzzleFlash:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.lifetime = 5
        self.size = random.randint(4, 6)
        
        # Flash colors
        self.colors = [
            (255, 200, 50),  # Yellow core
            (255, 150, 50),  # Orange mid
            (255, 100, 50)   # Red outer
        ]

    def update(self):
        self.lifetime -= 1
        self.size = max(2, self.size - 0.5)

    def draw(self, surface):
        if self.lifetime <= 0:
            return
            
        # Draw layered flash effect
        for i, color in enumerate(self.colors):
            size = self.size - i
            if size <= 0:
                continue
                
            alpha = int(255 * (self.lifetime / 5))
            flash_color = (*color, alpha)
            
            # Star shape
            points = []
            for j in range(8):
                angle = self.angle + (j * math.pi / 4)
                dist = size if j % 2 == 0 else size * 0.5
                px = self.x + math.cos(angle) * dist
                py = self.y + math.sin(angle) * dist
                points.append((px, py))
                
            pygame.draw.polygon(surface, flash_color, points)

class BulletParticleSystem:
    def __init__(self):
        self.bullets = []
        self.muzzle_flashes = []
        
    def shoot(self, start_pos, target_pos):
        """Create new bullet and muzzle flash"""
        # Calculate angle for muzzle flash
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        angle = math.atan2(dy, dx)
        
        # Create bullet
        self.bullets.append(Bullet(start_pos[0], start_pos[1], target_pos[0], target_pos[1]))
        
        # Create muzzle flash
        self.muzzle_flashes.append(MuzzleFlash(start_pos[0], start_pos[1], angle))
        
    def update(self):
        """Update all particles"""
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.dead:
                self.bullets.remove(bullet)
                
        # Update muzzle flashes
        for flash in self.muzzle_flashes[:]:
            flash.update()
            if flash.lifetime <= 0:
                self.muzzle_flashes.remove(flash)
                
    def draw(self, surface):
        """Draw all particles"""
        # Create a surface for additive blending
        particle_surface = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(particle_surface)
            
        # Draw muzzle flashes
        for flash in self.muzzle_flashes:
            flash.draw(particle_surface)
            
        # Blit with additive blending for glow effect
        surface.blit(particle_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD) 