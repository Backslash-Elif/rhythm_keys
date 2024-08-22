import pygame
#import sys

#colors
colorschemes = {
    1: [(200, 200, 200), (170, 170, 170)],
    2: [(33, 33, 33), (43, 43, 43)]
    }

class InputBox:
    def __init__(self, width: int, text_size: int, position: tuple, max_input_len: int, colorscheme: int = 1, pre_input: str = ""):
        self.width = width
        self.text_size = text_size
        self.position = position
        self.color, self.active_color = colorschemes[colorscheme]
        self.max_input_len = max_input_len
        self.input_text = pre_input
        self.active = False
        self.font = pygame.font.Font(None, self.text_size)
        self.rect = pygame.Rect(position[0], position[1], width, text_size + 10)

    def handle_event(self, event):
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
        txt_surface = self.font.render(self.input_text, True, (0, 0, 0))
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def get_text(self):
        return self.input_text

## Initialize Pygame
#pygame.init()
#screen = pygame.display.set_mode((640, 480))
#pygame.display.set_caption("Input Box Example")
#
## Create an instance of InputBox
#input_box = InputBox(width=300, text_size=32, position=(170, 200), color=(200, 200, 200), max_input_len=20, pre_input="haii")
#
## Main loop
#running = True
#while running:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            running = False
#        input_box.handle_event(event)
#
#    screen.fill((255, 255, 255))  # Clear the screen
#    input_box.draw(screen)          # Draw the input box
#    pygame.display.flip()           # Update the display
#
#pygame.quit()
#sys.exit()
#