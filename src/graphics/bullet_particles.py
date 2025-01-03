import pygame
import math

class Particle:
    def __init__(self, x, y, dx, dy, color, lifetime, size):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.lifetime = lifetime
        self.size = size
        self.alpha = 255

class BulletParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, dx, dy, color, lifetime, size):
        """Add a new particle to the system"""
        self.particles.append(Particle(x, y, dx, dy, color, lifetime, size))

    def update(self):
        """Update all particles"""
        # Update particle positions and lifetimes
        for particle in self.particles[:]:  # Create a copy to safely remove while iterating
            particle.x += particle.dx
            particle.y += particle.dy
            particle.lifetime -= 1
            # Fade out particle as it nears end of life
            particle.alpha = int(255 * (particle.lifetime / 10))
            
            # Remove dead particles
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            # Create a surface for the particle with alpha channel
            particle_surface = pygame.Surface((particle.size * 2, particle.size * 2), pygame.SRCALPHA)
            
            # Get color with alpha
            color_with_alpha = (*particle.color[:3], particle.alpha)
            
            # Draw the particle
            pygame.draw.circle(particle_surface, color_with_alpha, 
                             (particle.size, particle.size), particle.size)
            
            # Blit the particle surface onto the screen
            screen.blit(particle_surface, 
                       (particle.x - particle.size, particle.y - particle.size)) 