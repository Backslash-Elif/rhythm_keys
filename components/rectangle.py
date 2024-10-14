import pygame

class Rectangle:
    def __init__(self, position: tuple, size: tuple, color: tuple = (255, 0, 0), radius: int = 0) -> None:
        self.position = position
        self.size = size
        self.color = color
        self.radius = radius
        self._update_rect()
    
    def _update_rect(self):
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=self.radius)
    
    def set_position(self, new_position: tuple):
        self.position = new_position
        self._update_rect()
    
    def set_size(self, new_size: tuple):
        self.size = new_size
        self._update_rect()
    
    def set_color(self, new_color: tuple):
        self.color = new_color
    
    def set_radius(self, new_radius: int):
        self.radius = new_radius

    def get_position(self):
        return self.position

    def get_size(self):
        return self.size
    
    def get_color(self):
        return self.color
    
    def get_radius(self):
        return self.radius