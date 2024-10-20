import pygame

class Card:
    def __init__(self, position: tuple, size: tuple, color: tuple) -> None:
        self.srgb = color
        self.rgb = color[0:3] #cut alpha value
        self.position = position
        self.size = size

        #rectangle layout
        self.rect = pygame.Rect((0, 0), self.size)

        #create surface and prerender component
        self.buffer = pygame.Surface(self.size, pygame.SRCALPHA)

        #draw rectangles
        pygame.draw.rect(self.buffer, self.srgb, self.rect, border_radius=10)
        pygame.draw.rect(self.buffer, self.rgb, self.rect, 3, 10)

    def draw(self, surface):
        #draw prerendered surface onto main screen
        surface.blit(self.buffer, self.position)
    
    def get_size(self):
        return self.size

    def set_pos(self, new_position:tuple):
        self.position = new_position
    
    def set_color(self, new_color):
        self.srgb = new_color
        self.rgb = new_color[0:3]

        #create surface and prerender component
        self.buffer = pygame.Surface(self.size, pygame.SRCALPHA)
        
        #draw rectangles
        pygame.draw.rect(self.buffer, self.srgb, self.rect, border_radius=10)
        pygame.draw.rect(self.buffer, self.rgb, self.rect, 3, 10)