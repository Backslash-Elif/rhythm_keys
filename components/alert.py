import pygame, global_vars, screen_utils
from components import card, text, button, rectangle, inputbox
from components.styles import card_themes, UI_colors, CardThemeName, UIColorName, text_size, TextSizeName, colors, ColorName

class Alert:
    def __init__(self) -> None:
        self.fullscreencard = card.Card((0, 0), global_vars.const_rendersize, card_themes[CardThemeName.DARK])
        self.active = False
        self.alerttype = 0

        self.result = None

        self.buffer = pygame.Surface(global_vars.const_rendersize, pygame.SRCALPHA)
    
    def _render(self):
        self.buffer.fill((0, 0, 0, 0))
        self.fullscreencard.draw(self.buffer)
        self.msg_card.draw(self.buffer)
        self.text_object.draw(self.buffer)

    
    def new_alert(self, alert_text: str = "Internal error:\n\nNo alert text provided.", alert_type: int = 0): #0=OK, 1=Cancel & OK, 3=Input & Cancel & OK
        #styling:
        content_pos = (700, 400) #almost the middle, easier to calculate than actual middle
        content_size = (500, 300)
        
        self.msg_card = rectangle.Rectangle((690, 390), (520, 320), colors[ColorName.BLACK_GRAY][0] if global_vars.user_dark_mode else colors[ColorName.LIGHT_GRAY][0], 16, 3, (255, 255, 255) if global_vars.user_dark_mode else (0, 0, 0)) #rectangle is 10px bigger on all sides
        self.text_object = text.Text(alert_text, text_size[TextSizeName.TEXT], content_pos, content_size, colors[ColorName.DYNAMIC][0])
        self.confirm_buttonobject = button.Button("OK", text_size[TextSizeName.TEXT], (1050, 660), (100, 40), UI_colors[UIColorName.PRIMARY])
        self.cancel_buttonobject = button.Button("Cancel", text_size[TextSizeName.TEXT], (750, 660), (100, 40), UI_colors[UIColorName.DANGER])
        self.inputobject = inputbox.InputBox((content_size[0], 50), text_size[TextSizeName.TEXT], (700, 600), 32, UI_colors[UIColorName.SECONDARY])

        if alert_type == 2:
            self.text_object.set_size((content_size[0], 200))
        else:
            self.text_object.set_size((content_size[0], 250))
        
        self.active = True
        self.alerttype = alert_type
        self.result = None
        self._render()
    
    def handle_events(self, event):
        if self.confirm_buttonobject.is_clicked(event):
            self.active = False
            if self.alerttype != 2:
                self.result = True
            else:
                self.inputobject.get_text()
        if self.alerttype > 0:
            if self.cancel_buttonobject.is_clicked(event):
                self.active = False
                self.result = False
        if self.alerttype == 2:
            self.inputobject.handle_events(event)
    
    def draw(self, surface):
        if self.active:
            #blits the prerendered buffer to the given surface
            surface.blit(self.buffer, (0, 0))
            self.confirm_buttonobject.draw(surface) #draw directly cuz already prerendered
            if self.alerttype > 0:
                self.cancel_buttonobject.draw(surface)
            if self.alerttype == 2:
                self.inputobject.draw(surface)
    
    def is_active(self):
        return self.active
    
    def get_result(self):
        return self.result