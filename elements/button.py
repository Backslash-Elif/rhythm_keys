import pygame
#import sys
#
## Initialize Pygame
#pygame.init()
#
## Set up display
#screen = pygame.display.set_mode((800, 600))
#pygame.display.set_caption("Reusable Button Example")
#
## Define colors
#WHITE = (255, 255, 255)
#BLUE = (0, 0, 255)
#GREEN = (0, 255, 0)

#colors
colorschemes = {
    1: [(33, 33, 33), (43, 43, 43)],
    2: [(11, 87, 208), (30, 100, 212)],
    3: [(255, 0, 0), (204, 0, 0)]
    }

# Button class
class Button:
    def __init__(self, text, position, text_size, width, color_scheme=1):
        self.color, self.hover_color = colorschemes[color_scheme]
        self.text = text
        self.position = position
        self.text_size = text_size
        self.width = width
        self.font = pygame.font.Font(None, self.text_size)
        self.rect = pygame.Rect(position[0], position[1], width, self.text_size + 20)

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

# Main program to demonstrate the button
#def main():
#    button = Button(GREEN, "Click Me", (325, 250), 30, 150)
#
#    while True:
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                pygame.quit()
#                sys.exit()
#
#        # Check for mouse hover
#        mouse_pos = pygame.mouse.get_pos()
#        if button.is_hovered(mouse_pos):
#            button.color = BLUE
#        else:
#            button.color = GREEN
#
#        # Fill the screen with white
#        screen.fill(WHITE)
#
#        # Draw the button
#        button.draw(screen)
#
#        # Refresh the display
#        pygame.display.flip()
#        pygame.time.Clock().tick(60)  # Limit to 60 frames per second
#
#if __name__ == "__main__":
#    main()