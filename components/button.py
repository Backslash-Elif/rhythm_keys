import pygame, global_vars
from components import text, rectangle

class Button:
    def __init__(self, display_text: str, text_size: int, position: tuple, size: tuple, color_scheme: tuple, textallign: text.TextAlign = text.TextAlign.CENTER):
        self.color, self.hover_color, self.text_color = color_scheme #unpacking the colors
        self.text = display_text
        self.textalign = textallign
        self.position = position
        self.text_size = text_size
        self.width, self.height = size
        self.last_active = False #used to check if the active state changed since last frame
        #create objects
        self.text_object = text.Text(display_text, text_size, (0, 0), size, self.text_color, self.textalign) #position initialized with (0, 0) as size is unknown
        self.rectangleobject = rectangle.Rectangle((0, 0), (self.width, self.height), self.color, 10, 2, self.text_color)#position set to 0, 0 because of rendering to buffer screen
        self.hitbox = pygame.Rect(self.position[0], self.position[1], self.width, self.height) #hitbox rectangle at correct position for mouse interaction
        #create buffer screen with SRCALPHA (sRGB) params
        self.buffer = pygame.Surface(size, pygame.SRCALPHA)
        #render the compnent
        self._render()

    def _render(self): #prerenders the component to a buffer screen
        #draw rounded rectangle
        if self.hitbox.collidepoint(global_vars.get_mouse_pos()):
            self.rectangleobject.set_color(self.hover_color)
        else:
            self.rectangleobject.set_color(self.color)
        self.rectangleobject.draw(self.buffer)
        #update and draw the text object
        self.text_object.set_position(((self.width/2)-self.text_object.get_size()[0]/2, (self.height/2)-self.text_object.get_size()[1]/2))
        self.text_object.draw(self.buffer)

    def draw(self, surface):
        #blits the prerendered buffer to the given surface
        surface.blit(self.buffer, self.position)
    
    def is_clicked(self, event):#also the event handler because never only one of them gets checked
        #check if the active state has changed and if so, re-render the component
        if self.hitbox.collidepoint(global_vars.get_mouse_pos()) != self.last_active:
            self.last_active = not self.last_active
            self._render()
        
        #check if event is mouse button release and if it is within the hitbox rect
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  #1 = left mouse button
            return self.hitbox.collidepoint(global_vars.get_mouse_pos())
        return False
    
    def set_text(self, new_text: str):
        self.text_object.set_text(new_text)
        self._render()
    
    def set_color_scheme(self, new_color_scheme: tuple):
        self.color, self.hover_color, self.text_color = new_color_scheme
        self._render()
    
    def set_position(self, new_position: tuple):
        self.position = new_position
        self.hitbox = pygame.Rect(self.position[0], self.position[1], self.width, self.height) #update hitbox