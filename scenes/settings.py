import pygame, global_vars, tools
from scenes import scene

from components import button, debug, text, touchtrigger, bgstyle
from components.styles import colors, UI_colors, background_gradient, text_size, ColorName, UIColorName, TextSizeName

class Settings(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        
        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.sys_screen_size)

        #components
        self.title_textobject = text.Text("Settings", text_size[TextSizeName.TITLE], (100, 100), (400, 100), colors[ColorName.DYNAMIC][0])
        self.back_buttonobject = button.Button("Back", text_size[TextSizeName.TEXT], (50, 950), (100, 50), UI_colors[UIColorName.DANGER])
    
    def handle_event(self, event):
        if self.back_buttonobject.is_clicked(event):
            self.manager.switch_to_scene("Main menu")
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        self.title_textobject.draw(surface)
        self.back_buttonobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)