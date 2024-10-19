import global_vars
from scenes import scene

from components import button, debug, text, bgstyle, card, inputbox, alert
from components.styles import colors, UI_colors, background_gradient, text_size, ColorName, UIColorName, TextSizeName, card_themes, CardThemeName, BGGradientName, compute_dynamic_colors

class Results(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        
        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.const_rendersize)

        #components
        self.fg_cardobject = card.Card((200, 100), (1500, 800), card_themes[CardThemeName.DYNAMIC])
        self.title_textobject = text.Text("Settings", text_size[TextSizeName.TITLE], (300, 200), (400, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        
    
    def handle_event(self, event):
        print()
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        self.fg_cardobject.draw(surface)
        self.title_textobject.draw(surface)
        
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)