import pygame

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 32, 32)
        self.sprite = None
        
    def update(self):
        """Base update method"""
        pass
        
    def draw(self, screen):
        """Draw the entity"""
        if self.sprite:
            screen.blit(self.sprite, self.rect)
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.rect) 