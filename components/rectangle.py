import pygame

class Rectangle:
    def __init__(self, position: tuple, size: tuple, color: tuple = (255, 0, 0), radius: int = 0, border_width:int = 0, border_color:tuple = (0, 0, 0)) -> None:
        self.position = position
        self.size = size
        self.color = color
        self.radius = radius
        self.border = int(border_width)
        self.border_color = border_color
        self._update_rect()
    
    def _update_rect(self):
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=self.radius)
        if self.border > 0:
            pygame.draw.rect(surface, self.border_color, self.rect, width=self.border, border_radius=self.radius)
    
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

    def set_border_width(self, new_border_width):
        self.border = new_border_width
    def set_border_color(self, new_border_color):
        self.border_color = new_border_color
    def get_border_width(self):
        return self.border
    def get_border_color(self):
        return self.border_color