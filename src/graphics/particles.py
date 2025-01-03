import pygame
import random
import math

class FireParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.uniform(0.5, 1.5)  # Much smaller particles
        angle = random.uniform(-0.3, 0.3)  # Tighter spread
        speed = random.uniform(0.5, 1.5)  # Slower movement
        self.vx = math.sin(angle) * speed
        self.vy = -speed * random.uniform(0.8, 1.2)  # More consistent upward motion
        self.lifetime = random.randint(30, 50)  # Longer lifetime for smoother effect
        self.alpha = 180  # Lower initial alpha for subtlety
        self.color = random.choice([
            (255, 120, 20),   # Warm orange
            (255, 140, 40),   # Soft orange
            (255, 100, 10),   # Deep orange
            (255, 160, 60),   # Light orange
        ])
        self.dead = False
        self.flicker_offset = random.uniform(0, math.pi * 2)  # For smooth flickering

    def update(self):
        # Update position with velocity
        self.x += self.vx
        self.y += self.vy
        
        # Subtle flickering effect using sine wave
        flicker = math.sin(pygame.time.get_ticks() * 0.01 + self.flicker_offset) * 0.1
        self.x += flicker
        
        # Very gradual slowdown
        self.vy *= 0.98
        
        # Decrease lifetime and alpha with smooth fade
        self.lifetime -= 1
        progress = self.lifetime / 50  # Normalized lifetime
        self.alpha = int(180 * (progress * 0.8 + 0.2))  # Smoother fade out
        
        if self.lifetime <= 0:
            self.dead = True

    def get_color_with_alpha(self, alpha_override=None):
        """Get the particle color with proper alpha blending"""
        alpha = int(alpha_override if alpha_override is not None else self.alpha)
        return (int(self.color[0]), int(self.color[1]), int(self.color[2]), alpha)

class EmberParticle(FireParticle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = random.uniform(0.3, 0.8)  # Tiny embers
        self.color = random.choice([
            (255, 180, 60),   # Soft yellow
            (255, 140, 40),   # Warm orange
            (255, 200, 100),  # Pale yellow
        ])
        self.lifetime = random.randint(40, 60)
        # Gentler, more swirling movement
        angle = random.uniform(-math.pi, math.pi)
        speed = random.uniform(0.2, 0.6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - 0.5  # Slight upward drift
        self.spin = random.uniform(-0.1, 0.1)  # Add spinning motion

    def update(self):
        super().update()
        # Add gentle spinning motion
        angle = pygame.time.get_ticks() * self.spin
        self.vx = math.cos(angle) * 0.2
        self.vy = math.sin(angle) * 0.2 - 0.5

class SmokeParticle(FireParticle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = random.uniform(1.0, 2.0)  # Slightly larger but still subtle
        self.color = random.choice([
            (40, 40, 40),     # Very dark grey
            (50, 50, 50),     # Dark grey
            (60, 60, 60),     # Medium grey
        ])
        self.lifetime = random.randint(60, 80)  # Longer lifetime for smoke
        # Very slow, drifting movement
        self.vx = random.uniform(-0.2, 0.2)
        self.vy = -random.uniform(0.1, 0.3)
        self.alpha = 40  # Very transparent smoke

class BonfireParticleSystem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particles = []
        self.last_spawn = 0
        self.spawn_rate = 2  # Slower spawn rate for less density
        self.max_particles = 150  # More particles but smaller
        
    def update(self):
        # Spawn new particles if under limit
        if len(self.particles) < self.max_particles:
            self.last_spawn += 1
            if self.last_spawn >= self.spawn_rate:
                self.last_spawn = 0
                # Add different types of particles
                if random.random() < 0.6:  # 60% chance for fire particles
                    for _ in range(3):  # Multiple small particles
                        self.particles.append(FireParticle(
                            self.x + random.uniform(-2, 2),  # Slight position variation
                            self.y + random.uniform(-1, 1)
                        ))
                elif random.random() < 0.6:  # 24% chance for embers
                    self.particles.append(EmberParticle(
                        self.x + random.uniform(-1, 1),
                        self.y + random.uniform(-1, 1)
                    ))
                else:  # 16% chance for smoke
                    self.particles.append(SmokeParticle(
                        self.x + random.uniform(-2, 2),
                        self.y
                    ))
        
        # Update existing particles
        for particle in self.particles[:]:
            particle.update()
            if particle.dead:
                self.particles.remove(particle)

    def draw(self, surface):
        if not self.particles:
            return
            
        # Create a surface for additive blending
        particle_surface = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        
        # Draw all particles
        for particle in self.particles:
            try:
                # Create a subsurface for the glow effect
                glow_size = particle.size * 2  # Smaller glow
                glow_surface = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)
                
                # Draw the glow (larger, more transparent)
                glow_alpha = min(particle.alpha // 4, 60)  # More transparent glow
                glow_color = particle.get_color_with_alpha(glow_alpha)
                pygame.draw.circle(glow_surface, glow_color, 
                                 (int(glow_size), int(glow_size)), 
                                 int(glow_size))
                
                # Draw the particle core
                core_color = particle.get_color_with_alpha()
                pygame.draw.circle(glow_surface, core_color,
                                 (int(glow_size), int(glow_size)),
                                 max(1, int(particle.size)))  # Ensure minimum size of 1
                
                # Blit the particle with its glow
                pos = (int(particle.x - glow_size), int(particle.y - glow_size))
                particle_surface.blit(glow_surface, pos, special_flags=pygame.BLEND_RGBA_ADD)
            except (ValueError, TypeError) as e:
                continue
        
        # Blit the final particle surface to the main surface with reduced alpha
        surface.blit(particle_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD) 