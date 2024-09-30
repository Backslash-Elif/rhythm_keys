import global_vars, tools, global_vars
from scenes import scene

from components import button, debug, text, bgstyle
from components.styles import colors, UI_colors, background_gradient, ColorName, UIColorName, text_size, TextSizeName, BGGradientName

class MainMenu(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        
        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.const_rendersize)

        #components
        self.title_textobject = text.Text("Welcome to RHYTHM KEYS!", text_size[TextSizeName.LARGE_TITLE], (0, 150), (global_vars.const_rendersize[0], 100), colors[ColorName.SKY_BLUE][0])
        self.title_bg_textobject = text.Text("Welcome to RHYTHM KEYS!", text_size[TextSizeName.LARGE_TITLE]+2, (0, 150), (global_vars.const_rendersize[0], 100), colors[ColorName.LIGHT_BLUE][0]) #almost identical duplicate for effect
        self.play_buttonobject = button.Button("Play", text_size[TextSizeName.TEXT], tools.Screen.center_obj(global_vars.const_rendersize, (500, 75), (0, -100)), (500, 75), UI_colors[UIColorName.PRIMARY])
        self.editor_buttonobject = button.Button("Editor", text_size[TextSizeName.TEXT], tools.Screen.center_obj(global_vars.const_rendersize, (500, 75)), (500, 75), UI_colors[UIColorName.SECONDARY])
        self.settings_buttonobject = button.Button("Settings", text_size[TextSizeName.TEXT], tools.Screen.center_obj(global_vars.const_rendersize, (500, 75), (0, 100)), (500, 75), UI_colors[UIColorName.SECONDARY])
    
    def handle_event(self, event):
        if self.editor_buttonobject.is_clicked(event):
            self.manager.switch_to_scene("Editor main menu")
        if self.settings_buttonobject.is_clicked(event):
            self.manager.switch_to_scene("Settings")
    
    def draw(self, surface):
        if global_vars.user_bg_color == BGGradientName.NONE.value or len(global_vars.user_name) < 4:
            global_vars.sys_oobe = True
        if global_vars.sys_oobe:
            self.manager.switch_to_scene("OOBE")
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        self.title_bg_textobject.draw(surface)
        self.title_textobject.draw(surface)
        self.play_buttonobject.draw(surface)
        self.editor_buttonobject.draw(surface)
        self.settings_buttonobject.draw(surface)
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)