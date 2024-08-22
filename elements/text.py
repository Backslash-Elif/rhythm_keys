import pygame

class Text:
    def __init__(self, text: str, size: int, position: tuple, color:tuple = (255, 255, 255)) -> None:
        self.displaytext = text
        self.textsize = size
        self.textpos = position
        self.textcolor = color
    
    def set_text(self, newtext:str):
        self.displaytext = newtext
    
    def get_text(self):
        return self.displaytext
    
    def draw(self, surface):
        font = pygame.font.SysFont("Arial", self.textsize)
    
        # Render the text in white
        text_surface = font.render(self.displaytext, True, self.textcolor)
        
        # Blit the text onto the screen
        surface.blit(text_surface, self.textpos)