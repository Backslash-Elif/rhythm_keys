import pygame
from components import text

class InputBox:
    def __init__(self, size: tuple, text_size: int, position: tuple, max_input_len: int, colorscheme: list, pre_input: str = ""):
        self.width, self.height = size
        self.text_size = text_size
        self.position = position
        self.color, self.active_color, self.text_color = colorscheme
        self.max_input_len = max_input_len
        self.input_text = pre_input
        self.active = False

        self.text = text.Text(pre_input, text_size, (0, 0), self.text_color)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.hitbox = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

        self._render()
    
    def _render(self):
        self.text.set_text(self.input_text)
        self.text.set_position((5, self.height/2 - self.text.get_size()[1]/2))
        if self.active:
            pygame.draw.rect(self.surface, self.active_color, self.rect, border_radius=5)
        else:
            pygame.draw.rect(self.surface, self.color, self.rect, border_radius=5)
        self.text.draw(self.surface)

    def handle_events(self, event): #event handler
        update = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            update = True
            if self.hitbox.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.active = False
                    update = True
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]  # Remove the last character
                    update = True
                elif event.unicode and len(self.input_text) < self.max_input_len:
                    if len(repr(event.unicode)) == 3:
                        self.input_text += event.unicode
                        update = True
        
        if update:
            self._render()

    def draw(self, surface):
        # Draw the input box with different colors based on active state
        surface.blit(self.surface, self.position)

    def get_text(self):
        return self.input_text