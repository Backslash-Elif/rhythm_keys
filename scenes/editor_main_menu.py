import global_vars, screen_utils
from scenes import scene

from components import button, debug, text, bgstyle
from components.styles import colors, UI_colors, background_gradient, ColorName, UIColorName, text_size, TextSizeName

class EditorMainMenu(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        
        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.const_rendersize)

        global_vars.editor_load_vars = False

        #components
        self.title_text = text.Text("Welcome to the editor!", text_size[TextSizeName.LARGE_TITLE], (0, 150), (global_vars.const_rendersize[0], 100), colors[ColorName.GREEN][0])
        self.create_button = button.Button("Create New", text_size[TextSizeName.TEXT], screen_utils.center_obj(global_vars.const_rendersize, (500, 75), (0, -100)), (500, 75), UI_colors[UIColorName.PRIMARY])
        self.open_button = button.Button("Open...", text_size[TextSizeName.TEXT], screen_utils.center_obj(global_vars.const_rendersize, (500, 75)), (500, 75), UI_colors[UIColorName.SECONDARY])
        self.back_button = button.Button("Back", text_size[TextSizeName.TEXT], screen_utils.center_obj(global_vars.const_rendersize, (500, 75), (0, 100)), (500, 75), UI_colors[UIColorName.SECONDARY])
    
    def handle_event(self, event):
        if self.create_button.is_clicked(event):
            self.manager.switch_to_scene("Editor create menu")
        if self.back_button.is_clicked(event):
            self.manager.switch_to_scene("Main menu")
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        self.title_text.draw(surface)
        self.create_button.draw(surface)
        self.open_button.draw(surface)
        self.back_button.draw(surface)
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)