import pygame, global_vars
from components import text, rectangle

class InputBox:
    def __init__(self, size: tuple, text_size: int, position: tuple, max_input_len: int, colorscheme: tuple, pre_input: str = ""):
        self.width, self.height = size
        self.text_size = text_size
        self.position = position
        self.color, self.active_color, self.text_color = colorscheme #unpacking the colors
        self.max_input_len = max_input_len
        self.display_text = pre_input
        self.active = False #used to check if active
        #create objects
        self.text_object = text.Text(pre_input, text_size, (10, 0), (self.width-20, self.height), self.text_color, text.TextAlign.LEFT) #position initialized with (0, 0) as size is unknown
        self.rectangleobject = rectangle.Rectangle((0, 0), (self.width, self.height), self.color, 10, 2, self.text_color)#position set to 0, 0 because of rendering to buffer screen
        self.hitbox = pygame.Rect(self.position[0], self.position[1], self.width, self.height)#hitbox rectangle at correct position for mouse interaction
        #create buffer screen with SRCALPHA (sRGB) params
        self.buffer = pygame.Surface(size, pygame.SRCALPHA)

        self.cursor_counter = 60 #for blinking cursor
        self.cursor_state = False

        #render the component
        self._render()
    
    def _render(self):
        #update the text object
        self.text_object.set_text(self.display_text + ("|" if self.cursor_state else ""))
        self.text_object.set_position((5, self.height/2 - self.text_object.get_size()[1]/2))
        #draw the rect with correct color based on active condition
        if self.active:
            self.rectangleobject.set_color(self.active_color)
        else:
            self.rectangleobject.set_color(self.color)
        self.rectangleobject.draw(self.buffer)
        #draw textobject to buffer
        self.text_object.draw(self.buffer)

    def handle_events(self, event): #event handler
        update = False
        #check if mouse clicks on component
        if event.type == pygame.MOUSEBUTTONDOWN:
            update = True
            if self.hitbox.collidepoint(global_vars.get_mouse_pos()):
                self.active = True
                self.cursor_counter = 1
            else:
                self.cursor_counter = 60
                self.active = False

        #ad or remove characters
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.active = False
                    update = True
                    self.cursor_counter = 60
                elif event.key == pygame.K_BACKSPACE:
                    self.display_text = self.display_text[:-1]  # Remove the last character
                    update = True
                    self.cursor_counter = 1
                elif event.unicode and len(self.display_text) < self.max_input_len:
                    if len(repr(event.unicode)) == 3: #check if it's a printable character
                        self.display_text += event.unicode
                        self.cursor_counter = 1
                        update = True
        
        if update: #re-renders component if update
            self._render()

    def draw(self, surface):
        #blits the prerendered buffer to the given surface
        surface.blit(self.buffer, self.position)
        
        if self.active: #counts up
            self.cursor_counter += 1
            if self.cursor_counter > 60:
                self.cursor_counter = 1
        
        #update if curser needs to be toggled
        if self.cursor_counter <= 30 and not self.cursor_state:
            self.cursor_state = True
            self._render()
        if self.cursor_counter > 30 and self.cursor_state:
            self.cursor_state = False
            self._render()

    def get_text(self): #get method for display text
        return self.display_text
    
    def set_text(self, new_text: str): #set method for display text
        self.display_text = new_text
        self._render()