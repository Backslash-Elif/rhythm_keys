import pygame

class Text:
    def __init__(self, text: str, size: int, position: tuple, color:tuple = (255, 255, 255)) -> None:
        self.displaytext = text
        self.textsize = size
        self.textpos = position
        self.textcolor = color
        self.font = pygame.font.SysFont(None, self.textsize)
    
    def draw(self, surface): #draw to surface
        text_surface = self.font.render(self.displaytext, True, self.textcolor)
        
        # Blit the text onto the screen
        surface.blit(text_surface, self.textpos)
    
    def get_size(self):
        return self.font.size(self.displaytext)  # Returns (width, height)
    
    def get_text(self): #getter method text
        return self.displaytext
    
    def set_text(self, newtext:str): #setter method text
        self.displaytext = newtext
    
    def get_position(self): #getter method text position
        return self.textpos
    
    def set_position(self, newposition): #setter method text position
        self.textpos = newposition