import pygame
from components import text
from components.styles import colors, text_size, ColorName, TextSizeName

class DebugInfo:
    def __init__(self) -> None:
        self.info_text = text.Text("loading", text_size[TextSizeName.SMALL_TEXT], (0, 0), (300, 25), colors[ColorName.RED][0], text.TextAlign.TOP_LEFT)
    
    def draw(self, surface):
        self.info_text.set_text(f"Mouse: X={pygame.mouse.get_pos()[0]} Y={pygame.mouse.get_pos()[1]}")
        self.info_text.draw(surface)
        

class Grid:
    def __init__(self, screen_size):
        self.screen_size = screen_size

    def draw(self, surface):
        width, height = self.screen_size
        color1 = (255, 0, 0)
        color2 = (255, 150, 150)
        
        #vertical lines
        for i in range(0, width, 100):
            pygame.draw.line(surface, color2, (i+50, 0), (i+50, height)) #first the secondary color because of draw order
            pygame.draw.line(surface, color1, (i, 0), (i, height))
        
        #horizontal lines
        for i in range(0, height, 100):
            pygame.draw.line(surface, color2, (0, i+50), (width, i+50))
            pygame.draw.line(surface, color1, (0, i), (width, i))