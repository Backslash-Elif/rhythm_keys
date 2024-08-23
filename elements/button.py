import pygame

class Button:
    def __init__(self, text: str, text_size: int, position: tuple, width: int, height: int, color_scheme: list):
        self.color, self.hover_color = color_scheme
        self.text = text
        self.position = position
        self.text_size = text_size
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, self.text_size)
        self.rect = pygame.Rect(position[0], position[1], width, height)

    def draw(self, surface):
        # Draw rounded rectangle
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, self.hover_color, self.rect, border_radius=10)
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, event):
        # Check if the event is a mouse button RELEAASE
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # 1 = left mouse button
            # Check if the mouse position is over the rect
            return self.rect.collidepoint(event.pos)
        return False