import global_vars
from scenes import scene

from components import button, debug, text, bgstyle, inputbox, card, alert
from components.styles import colors, UI_colors, background_gradient, text_size, compute_dynamic_colors, ColorName, UIColorName, TextSizeName, BGGradientName, card_themes, CardThemeName

class OutOfBoxExperience(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        
        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.const_rendersize)

        #components
        self.fg_cardobject = card.Card((200, 100), (1500, 800), card_themes[CardThemeName.DYNAMIC])
        self.title_textobject = text.Text("Welcome to Rhythm Keys!", text_size[TextSizeName.TITLE], (300, 150), (900, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.BOTTOM_LEFT)
        self.subtitle_textobject = text.Text("Tell us a bit about yourself.", text_size[TextSizeName.SUBTITLE], (300, 250), (500, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.TOP_LEFT)
        self.username_textobject = text.Text("Username", text_size[TextSizeName.TEXT], (300, 350), (200, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.BOTTOM_LEFT)
        self.username_inputobject = inputbox.InputBox((500, 50), text_size[TextSizeName.SUBTITLE], (300, 400), 16, UI_colors[UIColorName.SECONDARY])
        self.darkmode_textobject = text.Text("Want a different theme?", text_size[TextSizeName.TEXT], (300, 500), (400, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.BOTTOM_LEFT)
        self.darkmode_buttonobject = button.Button(f"Switch to {'light' if global_vars.user_dark_mode else 'dark'} mode", text_size[TextSizeName.TEXT], (300, 550), (300, 50), UI_colors[UIColorName.SECONDARY])
        self.theme_textobject = text.Text("Choose your favourite theme!", text_size[TextSizeName.TEXT], (1050, 350), (550, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.BOTTOM)
        self.theme1_buttonobject = button.Button("Midnight", text_size[TextSizeName.TEXT], (1050, 400), (150, 100), colors[ColorName.DARK_BLUE])
        self.theme2_buttonobject = button.Button("Daybreak", text_size[TextSizeName.TEXT], (1250, 400), (150, 100), colors[ColorName.PURPLE])
        self.theme3_buttonobject = button.Button("Orchids", text_size[TextSizeName.TEXT], (1450, 400), (150, 100), colors[ColorName.PINK])
        self.theme4_buttonobject = button.Button("Peppermint", text_size[TextSizeName.TEXT], (1050, 550), (150, 100), colors[ColorName.LIGHT_GREEN])
        self.theme5_buttonobject = button.Button("Forrest", text_size[TextSizeName.TEXT], (1250, 550), (150, 100), colors[ColorName.DARK_GREEN])
        self.theme6_buttonobject = button.Button("Autumn", text_size[TextSizeName.TEXT], (1450, 550), (150, 100), colors[ColorName.ORANGE])
        self.theme7_buttonobject = button.Button("Ocean", text_size[TextSizeName.TEXT], (1050, 700), (150, 100), colors[ColorName.BLUE])
        self.theme8_buttonobject = button.Button("Mountain\nMist", text_size[TextSizeName.TEXT], (1250, 700), (150, 100), colors[ColorName.LIGHT_GRAY])
        self.theme9_buttonobject = button.Button("Cherry\nBlossom", text_size[TextSizeName.TEXT], (1450, 700), (150, 100), colors[ColorName.SOFT_RED])
        self.subtitle_textobject = text.Text("More settings cand be found\non the settings page.", text_size[TextSizeName.SMALL_TEXT], (300, 800), (300, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.TOP_LEFT)
        self.complete_buttonobject = button.Button("Complete", text_size[TextSizeName.TEXT], (300, 750), (150, 50), UI_colors[UIColorName.PRIMARY])
        self.alertobject = alert.Alert()

        #configure
        if "oobe_username" in global_vars.sys_persistant_storage:
            self.username_inputobject.set_text(global_vars.sys_persistant_storage["oobe_username"])
            del global_vars.sys_persistant_storage["oobe_username"]
    
    def handle_event(self, event):
        if self.alertobject.is_active():
            self.alertobject.handle_events(event)
        else:
            self.username_inputobject.handle_events(event)
            if self.darkmode_buttonobject.is_clicked(event):
                global_vars.sys_persistant_storage["oobe_username"] = self.username_inputobject.get_text()
                global_vars.user_dark_mode = not global_vars.user_dark_mode
                compute_dynamic_colors()
                self.manager.switch_to_scene("OOBE")
            if self.theme1_buttonobject.is_clicked(event):
                global_vars.user_bg_color = BGGradientName.MIDNIGHT.value
            if self.theme2_buttonobject.is_clicked(event):
                global_vars.user_bg_color = BGGradientName.DAYBREAK.value
            if self.theme3_buttonobject.is_clicked(event):
                global_vars.user_bg_color = BGGradientName.ORCHIDS.value
            if self.theme4_buttonobject.is_clicked(event):
                global_vars.user_bg_color = BGGradientName.PEPPERMINT.value
            if self.theme5_buttonobject.is_clicked(event):
                global_vars.user_bg_color = BGGradientName.FORREST.value
            if self.theme6_buttonobject.is_clicked(event):
                global_vars.user_bg_color = BGGradientName.AUTUMN.value
            if self.theme7_buttonobject.is_clicked(event):
                global_vars.user_bg_color = BGGradientName.OCEAN.value
            if self.theme8_buttonobject.is_clicked(event):
                global_vars.user_bg_color = BGGradientName.MOUNTAIN_MIST.value
            if self.theme9_buttonobject.is_clicked(event):
                global_vars.user_bg_color = BGGradientName.CHERRY_BLOSSOM.value
            if self.complete_buttonobject.is_clicked(event):
                if len(self.username_inputobject.get_text().strip()) < 4:
                    self.alertobject.new_alert("Please enter a valid Username.\n\n(Must be 4 or more and at most 15\ncharacters long.)")
                elif global_vars.user_bg_color == BGGradientName.NONE.value:
                    self.alertobject.new_alert("Please choose a theme.")
                else:
                    global_vars.user_name = self.username_inputobject.get_text()
                    global_vars.save_config()
                    global_vars.sys_oobe = False
                    self.manager.switch_to_scene("Main menu")
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        self.fg_cardobject.draw(surface)
        self.title_textobject.draw(surface)
        self.subtitle_textobject.draw(surface)
        self.username_textobject.draw(surface)
        self.username_inputobject.draw(surface)
        self.darkmode_textobject.draw(surface)
        self.darkmode_buttonobject.draw(surface)
        self.theme1_buttonobject.draw(surface)
        self.theme2_buttonobject.draw(surface)
        self.theme3_buttonobject.draw(surface)
        self.theme4_buttonobject.draw(surface)
        self.theme5_buttonobject.draw(surface)
        self.theme6_buttonobject.draw(surface)
        self.theme7_buttonobject.draw(surface)
        self.theme8_buttonobject.draw(surface)
        self.theme9_buttonobject.draw(surface)
        self.complete_buttonobject.draw(surface)
        self.alertobject.draw(surface)
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)