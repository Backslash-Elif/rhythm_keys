import global_vars
from scenes import scene

from components import button, debug, text, bgstyle, card, inputbox, alert, rectangle
from components.styles import colors, UI_colors, background_gradient, text_size, ColorName, UIColorName, TextSizeName, card_themes, CardThemeName, BGGradientName, compute_dynamic_colors

class Settings(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        
        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.const_rendersize)

        #components
        self.fg_cardobject = card.Card((200, 100), (1500, 800), card_themes[CardThemeName.DYNAMIC])
        self.title_textobject = text.Text("Settings", text_size[TextSizeName.TITLE], (300, 200), (400, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.back_buttonobject = button.Button("Back", text_size[TextSizeName.TEXT], (50, 950), (100, 50), UI_colors[UIColorName.DANGER])
        self.username_textobject = text.Text("Username", text_size[TextSizeName.TEXT], (300, 350), (200, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.BOTTOM_LEFT)
        self.username_inputobject = inputbox.InputBox((500, 50), text_size[TextSizeName.SUBTITLE], (300, 400), 16, UI_colors[UIColorName.SECONDARY], global_vars.user_name)
        self.darkmode_buttonobject = button.Button(f"Switch to {'light' if global_vars.user_dark_mode else 'dark'} mode", text_size[TextSizeName.TEXT], (300, 550), (300, 50), UI_colors[UIColorName.SECONDARY])
        self.theme1_buttonobject = button.Button("Midnight", text_size[TextSizeName.TEXT], (1400, 270), (200, 50), colors[ColorName.DARK_BLUE])
        self.theme2_buttonobject = button.Button("Daybreak", text_size[TextSizeName.TEXT], (1400, 330), (200, 50), colors[ColorName.PURPLE])
        self.theme3_buttonobject = button.Button("Orchids", text_size[TextSizeName.TEXT], (1400, 390), (200, 50), colors[ColorName.PINK])
        self.theme4_buttonobject = button.Button("Peppermint", text_size[TextSizeName.TEXT], (1400, 450), (200, 50), colors[ColorName.LIGHT_GREEN])
        self.theme5_buttonobject = button.Button("Forrest", text_size[TextSizeName.TEXT], (1400, 510), (200, 50), colors[ColorName.DARK_GREEN])
        self.theme6_buttonobject = button.Button("Autumn", text_size[TextSizeName.TEXT], (1400, 570), (200, 50), colors[ColorName.ORANGE])
        self.theme7_buttonobject = button.Button("Ocean", text_size[TextSizeName.TEXT], (1400, 630), (200, 50), colors[ColorName.BLUE])
        self.theme8_buttonobject = button.Button("Mountain Mist", text_size[TextSizeName.TEXT], (1400, 690), (200, 50), colors[ColorName.LIGHT_GRAY])
        self.theme9_buttonobject = button.Button("Cherry Blossom", text_size[TextSizeName.TEXT], (1400, 750), (200, 50), colors[ColorName.SOFT_RED])
        self.scale_textobject = text.Text("Window scaling", text_size[TextSizeName.TEXT], (900, 500), (300, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.BOTTOM)
        self.scale0_buttonobject = button.Button("720p\n(Downscaled)", text_size[TextSizeName.SMALL_TEXT], (900, 550), (150, 100), colors[ColorName.GRAY])
        self.scale1_buttonobject = button.Button("1080p (native)", text_size[TextSizeName.TEXT], (900, 550), (200, 150), colors[ColorName.DARK_GRAY] if global_vars.user_dark_mode else colors[ColorName.LIGHT_GRAY], text.TextAlign.BOTTOM)
        self.scale2_buttonobject = button.Button("1440p (Upscaled)", text_size[TextSizeName.TEXT], (900, 550), (250, 200), colors[ColorName.GRAY], text.TextAlign.BOTTOM)
        self.scale3_buttonobject = button.Button("4k (Upscaled a lot)", text_size[TextSizeName.TEXT], (900, 550), (300, 250), colors[ColorName.DARK_GRAY] if global_vars.user_dark_mode else colors[ColorName.LIGHT_GRAY], text.TextAlign.BOTTOM)
        self.alertobject = alert.Alert()

        self.creds_cardobject = card.Card((0, 0), global_vars.const_rendersize, card_themes[CardThemeName.DARK])
        self.creds_buttonobject = button.Button("About...", text_size[TextSizeName.TEXT], (1700, 950), (150, 50), UI_colors[UIColorName.SECONDARY])
        self.creds_rectangleobject = rectangle.Rectangle((200, 100), (1500, 800), UI_colors[UIColorName.SECONDARY][0], 15, 3, colors[ColorName.DYNAMIC][0])
        self.creds1_textobject = text.Text("A bame by", text_size[TextSizeName.LARGE_TITLE], (300, 200), (1300, 100), colors[ColorName.DYNAMIC][0])
        self.creds2_textobject = text.Text("Backs\\ash Studios", text_size[TextSizeName.TITLE], (300, 300), (1300, 100), colors[ColorName.DYNAMIC][0])
        self.creds3_textobject = text.Text("Playtesters:", text_size[TextSizeName.SMALL_TITLE], (300, 450), (600, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.creds4_textobject = text.Text("Oliver\nZifjon", text_size[TextSizeName.SUBTITLE], (300, 550), (600, 200), colors[ColorName.DYNAMIC][0], text.TextAlign.TOP_LEFT)
        self.creds5_textobject = text.Text("Sources:", text_size[TextSizeName.SMALL_TITLE], (1000, 450), (600, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.creds6_textobject = text.Text("pygame: www.pygame.org\n\nIcons:\ncustom-icon-design @ www.iconarchive.com\nsmashicons @ www.freepik.com", text_size[TextSizeName.TEXT], (1000, 550), (600, 200), colors[ColorName.DYNAMIC][0], text.TextAlign.TOP_LEFT)
        self.creds7_textobject = text.Text("- Backslash Studios (2024) -", text_size[TextSizeName.SMALL_TEXT], (200, 850), (1500, 50), colors[ColorName.DYNAMIC][0])
        self.credsactive = False

        #configure
        if "settings_username" in global_vars.sys_persistant_storage:
            self.username_inputobject.set_text(global_vars.sys_persistant_storage["settings_username"])
            del global_vars.sys_persistant_storage["settings_username"]
    
    def handle_event(self, event):
        if self.alertobject.is_active():
            self.alertobject.handle_events(event)
        elif not self.credsactive: #events aren't handled when alert is active
            self.username_inputobject.handle_events(event)

            #all the different themes
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

            if self.darkmode_buttonobject.is_clicked(event): #darkmode button; components can't dynamically switch to darmode so the new colors are computed and then the scene reloaded
                global_vars.sys_persistant_storage["settings_username"] = self.username_inputobject.get_text()
                global_vars.user_dark_mode = not global_vars.user_dark_mode
                compute_dynamic_colors()
                self.manager.switch_to_scene("Settings")

            #screen scales
            if self.scale0_buttonobject.is_clicked(event):
                self.manager.set_screensize(0)
            elif self.scale1_buttonobject.is_clicked(event):
                self.manager.set_screensize(1)
            elif self.scale2_buttonobject.is_clicked(event):
                self.manager.set_screensize(2)
            elif self.scale3_buttonobject.is_clicked(event):
                self.manager.set_screensize(3)

            if self.back_buttonobject.is_clicked(event): #back button & validation
                if len(self.username_inputobject.get_text()) < 4:
                    self.alertobject.new_alert("Please enter a valid Username.\n\n(Must be 4 or more and at most 15\ncharacters long.)")
                else:
                    global_vars.user_name = self.username_inputobject.get_text()
                    global_vars.save_config()
                    self.manager.switch_to_scene("Main menu")
            
        if self.creds_buttonobject.is_clicked(event):
            self.credsactive = not self.credsactive
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color]) #draws background

        self.fg_cardobject.draw(surface)
        self.title_textobject.draw(surface)
        self.back_buttonobject.draw(surface)
        self.username_textobject.draw(surface)
        self.username_inputobject.draw(surface)
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
        self.scale_textobject.draw(surface)
        self.scale3_buttonobject.draw(surface)#reverse for drawing order
        self.scale2_buttonobject.draw(surface)
        self.scale1_buttonobject.draw(surface)
        self.scale0_buttonobject.draw(surface)

        self.creds_buttonobject.draw(surface)
        if self.credsactive:
            self.creds_cardobject.draw(surface)
            self.creds_buttonobject.draw(surface)
            self.creds_rectangleobject.draw(surface)
            self.creds1_textobject.draw(surface)
            self.creds2_textobject.draw(surface)
            self.creds3_textobject.draw(surface)
            self.creds4_textobject.draw(surface)
            self.creds5_textobject.draw(surface)
            self.creds6_textobject.draw(surface)
            self.creds7_textobject.draw(surface)

        self.alertobject.draw(surface)

        #draws debug info
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)