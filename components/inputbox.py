import pygame, global_vars
from components import text

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
        self.rect = pygame.Rect(0, 0, self.width, self.height) #position set to 0, 0 because of rendering to buffer screen
        self.hitbox = pygame.Rect(self.position[0], self.position[1], self.width, self.height)#hitbox rectangle at correct position for mouse interaction
        #create buffer screen with SRCALPHA (sRGB) params
        self.buffer = pygame.Surface(size, pygame.SRCALPHA)
        #render the component
        self._render()
    
    def _render(self):
        #update the text object
        self.text_object.set_text(self.display_text)
        self.text_object.set_position((5, self.height/2 - self.text_object.get_size()[1]/2))
        #draw the rect with correct color based on active condition
        if self.active:
            pygame.draw.rect(self.buffer, self.active_color, self.rect, border_radius=5)
        else:
            pygame.draw.rect(self.buffer, self.color, self.rect, border_radius=5)
        #draw textobject to buffer
        self.text_object.draw(self.buffer)

    def handle_events(self, event): #event handler
        update = False
        #check if mouse clicks on component
        if event.type == pygame.MOUSEBUTTONDOWN:
            update = True
            if self.hitbox.collidepoint(global_vars.get_mouse_pos()):
                self.active = True
            else:
                self.active = False

        #ad or remove characters
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.active = False
                    update = True
                elif event.key == pygame.K_BACKSPACE:
                    self.display_text = self.display_text[:-1]  # Remove the last character
                    update = True
                elif event.unicode and len(self.display_text) < self.max_input_len:
                    if len(repr(event.unicode)) == 3: #check if it's a printable character
                        self.display_text += event.unicode
                        update = True
        
        if update: #re-renders component if update
            self._render()

    def draw(self, surface):
        #blits the prerendered buffer to the given surface
        surface.blit(self.buffer, self.position)

    def get_text(self): #get method for display text
        return self.display_text
    
    def set_text(self, new_text: str): #set method for display text
        self.display_text = new_text
        self._render()