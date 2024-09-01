import pygame, global_vars, tools
from components import card, text, button
from components.styles import Styles

class Alert:
    def __init__(self) -> None:
        self.fullscreencard = card.Card((0, 0), global_vars.sys_screen_size, Styles.card.dark())
        self.msg_card = None
        self.text_object = text.Text("No alert text provided XwX", 32, (0, 0))
        self.action_btn = button.Button("OK", 48, (0, 0), (128, 64), Styles.button.primary())
        self.active = False

        self.buffer = pygame.Surface(global_vars.sys_screen_size, pygame.SRCALPHA)
    
    def _render(self):
        self.buffer.fill((0, 0, 0, 0))
        self.fullscreencard.draw(self.buffer)
        self.msg_card.draw(self.buffer)
        self.text_object.draw(self.buffer)
    
    def new_alert(self, alert_text: str):
        self.text_object.set_text(alert_text)
        self.text_object.set_position(tools.Screen.center_obj(global_vars.sys_screen_size, self.text_object.get_size()))
        card_size = (self.text_object.get_size()[0]+100, self.text_object.get_size()[1]+200)
        self.msg_card = card.Card(tools.Screen.center_obj(global_vars.sys_screen_size, card_size), card_size, Styles.card.attention())
        self.action_btn.set_position((tools.Screen.center_axis(global_vars.sys_screen_size[0], 128), (global_vars.sys_screen_size[1]/2)+(card_size[1]/2-(64+16))))
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
        