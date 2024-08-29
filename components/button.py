import pygame
from components import text

class Button:
    def __init__(self, display_text: str, text_size: int, position: tuple, size: tuple, color_scheme: tuple):
        self.color, self.hover_color, self.text_color = color_scheme #unpacking the colors
        self.text = display_text
        self.position = position
        self.text_size = text_size
        self.width, self.height = size
        self.last_active = False #used to check if the active state changed since last frame
        #create objects
        self.text_object = text.Text(display_text, text_size, (0, 0), self.text_color) #position initialized with (0, 0) as size is unknown
        self.rect = pygame.Rect(0, 0, self.width, self.height) #position set to 0, 0 because of rendering to buffer screen
        self.hitbox = pygame.Rect(self.position[0], self.position[1], self.width, self.height) #hitbox rectangle at correct position for mouse interaction
        #create buffer screen with SRCALPHA (sRGB) params
        self.buffer = pygame.Surface(size, pygame.SRCALPHA)
        #render the compnent
        self._render()

    def _render(self): #prerenders the component to a buffer screen
        #draw rounded rectangle
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.buffer, self.hover_color, self.rect, border_radius=10)
        else:
            pygame.draw.rect(self.buffer, self.color, self.rect, border_radius=10)
        #update and draw the text object
        self.text_object.set_position(((self.width/2)-self.text_object.get_size()[0]/2, (self.height/2)-self.text_object.get_size()[1]/2))
        self.text_object.draw(self.buffer)

    def draw(self, surface):
        #check if the active state has changed and if so, re-render the component
        if self.hitbox.collidepoint(pygame.mouse.get_pos()) != self.last_active:
            self.last_active = not self.last_active
            self._render()
        
        #blits the prerendered buffer to the given surface
        surface.blit(self.buffer, self.position)
    
    def is_clicked(self, event):
        #check if event is mouse button release and if it is within the hitbox rect
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  #1 = left mouse button
            return self.hitbox.collidepoint(event.pos)
        return False