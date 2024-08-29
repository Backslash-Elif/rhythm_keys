import pygame

class Text:
    def __init__(self, text: str, size: int, position: tuple, color:tuple = (255, 255, 255)) -> None:
        self.display_text = text
        self.text_size = size
        self.position = position
        self.text_color = color

        self.font = pygame.font.SysFont(None, self.text_size) #font set to None for pygame built-in font
    
    def draw(self, surface): #draw to surface
        text_surface = self.font.render(self.display_text, True, self.text_color)
        #blit the text onto given surface
        surface.blit(text_surface, self.position)
    
    def get_size(self): #gets the size of the text
        return self.font.size(self.display_text)  #(width, height)
    
    def get_text(self): #getter method text
        return self.display_text
    
    def set_text(self, newtext:str): #setter method text
        self.display_text = newtext
    
    def get_position(self): #getter method text position
        return self.position
    
    def set_position(self, newposition: tuple): #setter method text position
        self.position = newposition