import pygame, global_vars, tools
from scenes import scene

from components import button, text, touchtrigger, fpscounter, bgstyle
from components.styles import colors, UI_colors, background_gradient

class MainMenu(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        #fps stuff
        self.fps_toggle = touchtrigger.Touchtrigger((0, 0), (256, 24))
        self.show_fps = False
        self.fps = fpscounter.Fpscounter()
        self.info_text = text.Text("loading", 24, (0, 0))
        #components
        self.title_textobject = text.Text("Welcome to RHYTHM KEYS!", 128, (0, 175), colors["sky_blue"][0])
        self.title_bg_textobject = text.Text("Welcome to RHYTHM KEYS!", 130, (0, 175), colors["light_blue"][0])
        self.play_buttonobject = button.Button("Play", 32, tools.Screen.center_obj(global_vars.sys_screen_size, (512, 64), (0, -72)), (512, 64), UI_colors["primary"])
        self.editor_buttonobject = button.Button("Editor", 32, tools.Screen.center_obj(global_vars.sys_screen_size, (512, 64)), (512, 64), UI_colors["secondary"])
        self.settings_buttonobject = button.Button("Settings", 32, tools.Screen.center_obj(global_vars.sys_screen_size, (512, 64), (0, 72)), (512, 64), UI_colors["secondary"])
        #configure components
        self.title_textobject.set_position((tools.Screen.center_axis(global_vars.sys_screen_size[0], self.title_textobject.get_size()[0]), self.title_textobject.get_position()[1]))
        self.title_bg_textobject.set_position((tools.Screen.center_axis(global_vars.sys_screen_size[0], self.title_bg_textobject.get_size()[0]), self.title_bg_textobject.get_position()[1]))
    
    def handle_event(self, event):
        if self.fps_toggle.update(event):
            self.show_fps = not self.show_fps
        if self.editor_buttonobject.is_clicked(event):
            self.manager.switch_to_scene("Editor main menu")
        if self.settings_buttonobject.is_clicked(event):
            self.manager.switch_to_scene("Settings")
    
    def draw(self, surface):
        if global_vars.sys_oobe:
            self.manager.switch_to_scene("OOBE")
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        if self.show_fps:
            self.info_text.set_text(f"FPS: {self.fps.get_fps()}, Mouse: X={pygame.mouse.get_pos()[0]} Y={pygame.mouse.get_pos()[1]}")
            self.info_text.draw(surface)
        self.title_bg_textobject.draw(surface)
        self.title_textobject.draw(surface)
        self.play_buttonobject.draw(surface)
        self.editor_buttonobject.draw(surface)
        self.settings_buttonobject.draw(surface)
    
    def update(self):
        self.fps.tick()