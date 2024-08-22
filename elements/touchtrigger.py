import pygame

class Touchtrigger:
    def __init__(self, location: tuple, size: tuple) -> None:
        self.location = location
        self.size = size
        self.font = pygame.font.Font(None, 24)

        # Create a rectangle for collision detection
        self.rect = pygame.Rect(self.location, self.size)

        # Create a surface for the trigger (invisible)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.fill((255, 255, 255, 0))  # Fully transparent

    def update(self, event):
        # Check if the event is a mouse button RELEASE
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # 1 = left mouse button
            # Check if the mouse position is over the rect
            if self.rect.collidepoint(event.pos):
                return True  # Trigger activated
        return False

    def draw_debug(self, surface, name: str = ""):
        # Draw the transparent surface for debugging
        surface.blit(self.surface, self.location)
        # Draw the outline of the rectangle
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 5)
        name_surface = self.font.render(name, True, (255, 255, 255))  # White text
        surface.blit(name_surface, (self.location[0] + 5, self.location[1] + 5))