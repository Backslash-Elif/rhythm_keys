import pygame

class Card:
    def __init__(self, location: tuple, size: tuple, color: tuple) -> None:
        self.srgb = color
        self.rgb = color[0:3]
        self.location = location
        self.size = size

        # rectangle layout
        self.rect = pygame.Rect((0, 0), self.size)

        # Create surface and pre-render card
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surface, self.srgb, self.rect, border_radius=10)
        pygame.draw.rect(self.surface, self.rgb, self.rect, 3, 10)

    def draw(self, surface):
        # Draw pre-rendered surface onto main screen
        surface.blit(self.surface, self.location)