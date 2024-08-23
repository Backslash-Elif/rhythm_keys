import pygame

class InputBox:
    def __init__(self, width: int, height: int, text_size: int, position: tuple, max_input_len: int, colorscheme: list, pre_input: str = ""):
        self.width = width
        self.height = height
        self.text_size = text_size
        self.position = position
        self.color, self.active_color, self.text_color = colorscheme
        self.max_input_len = max_input_len
        self.input_text = pre_input
        self.active = False
        self.font = pygame.font.Font(None, self.text_size)
        self.rect = pygame.Rect(position[0], position[1], width, height)

    def handle_events(self, event): #event handler
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]  # Remove the last character
                elif event.unicode and len(self.input_text) < self.max_input_len:
                    if len(repr(event.unicode)) == 3:
                        self.input_text += event.unicode

    def draw(self, screen):
        # Draw the input box with different colors based on active state
        color_to_use = self.active_color if self.active else self.color
        pygame.draw.rect(screen, color_to_use, self.rect, border_radius=5)
        txt_surface = self.font.render(self.input_text, True, self.text_color)
        screen.blit(txt_surface, (self.rect.x + 5, txt_surface.get_rect(center=self.rect.center)[1]))

    def get_text(self):
        return self.input_text