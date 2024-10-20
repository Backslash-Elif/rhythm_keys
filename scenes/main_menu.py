import global_vars, utils, global_vars
from scenes import scene

from components import button, debug, text, bgstyle, key_reader
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
        self.play_buttonobject = button.Button("Play", text_size[TextSizeName.TEXT], utils.center_obj(global_vars.const_rendersize, (500, 75), (0, -100)), (500, 75), UI_colors[UIColorName.PRIMARY])
        self.editor_buttonobject = button.Button("Editor", text_size[TextSizeName.TEXT], utils.center_obj(global_vars.const_rendersize, (500, 75)), (500, 75), UI_colors[UIColorName.SECONDARY])
        self.import_buttonobject = button.Button("Leveldata Management", text_size[TextSizeName.TEXT], utils.center_obj(global_vars.const_rendersize, (500, 75), (0, 100)), (500, 75), UI_colors[UIColorName.SECONDARY])
        self.settings_buttonobject = button.Button("Settings", text_size[TextSizeName.TEXT], utils.center_obj(global_vars.const_rendersize, (500, 75), (0, 200)), (500, 75), UI_colors[UIColorName.SECONDARY])

        #konami code for toggling the debug view
        self.konami = ("up", "up", "down", "down", "left", "right", "left", "right", "b", "a")
        self.konami_stage = 0

        self.keyreaderobject = key_reader.KeyReader()
    
    def handle_event(self, event):
        if self.play_buttonobject.is_clicked(event): #play button
            global_vars.sys_persistant_storage["select_destination"] = 2
            self.manager.switch_to_scene("Level selector")

        if self.editor_buttonobject.is_clicked(event): #editor button
            self.manager.switch_to_scene("Editor main menu")

        if self.import_buttonobject.is_clicked(event): # data manager button
            self.manager.switch_to_scene("Data manager")

        if self.settings_buttonobject.is_clicked(event): #settings button
            self.manager.switch_to_scene("Settings")
        
        #konami code detection
        new_key = self.keyreaderobject.get_pressed_key(event)
        if new_key != None:
            if new_key == self.konami[self.konami_stage]:
                self.konami_stage += 1
                if self.konami_stage > 9:
                    global_vars.sys_debug_lvl = 2 if global_vars.sys_debug_lvl == 0 else 0
                    self.konami_stage = 0
            else:
                self.konami_stage = 0
    
    def draw(self, surface):
        if global_vars.user_bg_color == BGGradientName.NONE.value or len(global_vars.user_name) < 4: #detects if OOBE was run yet or not
            global_vars.sys_oobe = True
        if global_vars.sys_oobe:
            self.manager.switch_to_scene("OOBE") #redirects to OOBE (Out Of Box Experience) (did definitely not rip that from windows)

        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color]) #draws background

        self.title_bg_textobject.draw(surface)
        self.title_textobject.draw(surface)
        self.play_buttonobject.draw(surface)
        self.editor_buttonobject.draw(surface)
        self.import_buttonobject.draw(surface)
        self.settings_buttonobject.draw(surface)

        #draws debug info
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)