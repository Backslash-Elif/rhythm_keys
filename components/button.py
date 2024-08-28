import pygame
from components import text

class Button:
    def __init__(self, displaytext: str, text_size: int, position: tuple, size: tuple, color_scheme: list):
        self.color, self.hover_color, self.text_color = color_scheme
        self.text = displaytext
        self.position = position
        self.text_size = text_size
        self.width, self.height = size
        self.lastactive = False
        self.textobject = text.Text(displaytext, text_size, (0, 0), self.text_color)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.hitbox = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

        self.buffer = pygame.Surface(size, pygame.SRCALPHA)

        self._render()

    def _render(self):
        # Draw rounded rectangle
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.buffer, self.hover_color, self.rect, border_radius=10)
        else:
            pygame.draw.rect(self.buffer, self.color, self.rect, border_radius=10)
        self.textobject.set_position(((self.width/2)-self.textobject.get_size()[0]/2, (self.height/2)-self.textobject.get_size()[1]/2))
        self.textobject.draw(self.buffer)

    def draw(self, surface):
        surface.blit(self.buffer, self.position)

    def handle_events(self, event):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()) != self.lastactive:
            self.lastactive = not self.lastactive
            self._render()
    
    def is_clicked(self, event):
        # Check if the event is a mouse button RELEAASE
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # 1 = left mouse button
            # Check if the mouse position is over the rect
            return self.hitbox.collidepoint(event.pos)
        return False