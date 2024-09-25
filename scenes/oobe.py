import pygame, global_vars, tools
from scenes import scene

from components import button, debug, text, touchtrigger, bgstyle, inputbox
from components.styles import colors, UI_colors, background_gradient, text_size, compute_dynamic_colors, ColorName, UIColorName, TextSizeName, BGGradientName

class OutOfBoxExperience(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        
        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.sys_screen_size)

        #components
        self.title_textobject = text.Text("Welcome to rhythm keys!", text_size[TextSizeName.TITLE], (100, 100), (100, 100), colors[ColorName.BLACK][0])
        self.subtitle_textobject = text.Text("Tell us a bit about yourself", text_size[TextSizeName.SUBTITLE], (100, 200), (100, 100), colors[ColorName.BLACK][0])
        self.username_textobject = text.Text("Username", text_size[TextSizeName.TEXT], (100, 280), (100, 100), colors[ColorName.GRAY][0])
        self.username_inputobject = inputbox.InputBox((500, 50), text_size[TextSizeName.SUBTITLE], (100, 300), 16, UI_colors[UIColorName.SECONDARY])
        self.darkmode_buttonobject = button.Button("Switch to dark mode", text_size[TextSizeName.TEXT], (100, 500), (300, 50), UI_colors[UIColorName.SECONDARY])

        #configure
        if "oobe_username" in global_vars.sys_persistant_storage:
            self.username_inputobject.set_text(global_vars.sys_persistant_storage["oobe_username"])
            del global_vars.sys_persistant_storage["oobe_username"]
    
    def handle_event(self, event):
        self.username_inputobject.handle_events(event)
        if self.darkmode_buttonobject.is_clicked(event):
            global_vars.sys_persistant_storage["oobe_username"] = self.username_inputobject.get_text()
            global_vars.user_dark_mode = not global_vars.user_dark_mode
            compute_dynamic_colors()
            self.manager.switch_to_scene("OOBE")
            
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        self.title_textobject.draw(surface)
        self.subtitle_textobject.draw(surface)
        self.username_textobject.draw(surface)
        self.username_inputobject.draw(surface)
        self.darkmode_buttonobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)