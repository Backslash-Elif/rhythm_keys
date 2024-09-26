import pygame, global_vars, tools
from components import card, text, button
from components.styles import card_themes, UI_colors, CardThemeName, UIColorName

class Alert:
    def __init__(self) -> None:
        self.fullscreencard = card.Card((0, 0), global_vars.sys_screen_size, card_themes[CardThemeName.DARK])
        self.msg_card = None
        self.text_object = text.Text("No alert text provided XwX", 32, (0, 0), (100, 100))
        self.action_btn = button.Button("OK", 32, (0, 0), (64, 32), UI_colors[UIColorName.PRIMARY])
        self.active = False

        self.buffer = pygame.Surface(global_vars.sys_screen_size, pygame.SRCALPHA)
    
    def _render(self):
        self.buffer.fill((0, 0, 0, 0))
        self.fullscreencard.draw(self.buffer)
        self.msg_card.draw(self.buffer)
        self.text_object.draw(self.buffer)
    
    def new_alert(self, alert_text: str): #creates alert
        #styling:
        card_size = (500, 300)
        self.text_object.set_text(alert_text)
        text_pos = tools.Screen.center_obj(global_vars.sys_screen_size, (card_size[0]-20, card_size[1]-20))
        self.text_object.set_size((card_size[0]-20, card_size[1]-20))
        self.text_object.set_position((text_pos[0], text_pos[1]))
        print(self.text_object.get_position(), self.text_object.get_size())
        self.msg_card = card.Card(tools.Screen.center_obj(global_vars.sys_screen_size, card_size), card_size, card_themes[CardThemeName.WARNING])
        self.action_btn.set_position((tools.Screen.center_axis(global_vars.sys_screen_size[0], 64), (global_vars.sys_screen_size[1]/2)+(card_size[1]/2-(32+16))))
        self.active = True
        self._render()
    
    def handle_events(self, event):
        if self.action_btn.is_clicked(event):
            self.active = False
    
    def draw(self, surface):
        if self.active:
            #blits the prerendered buffer to the given surface
            surface.blit(self.buffer, (0, 0))
            self.action_btn.draw(surface) #draw directly cuz already prerendered
    
    def is_active(self):
        return self.active