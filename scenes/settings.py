import pygame, global_vars, tools
from scenes import scene

from components import button, text, touchtrigger, fpscounter, bgstyle
from components.styles import colors, UI_colors, background_gradient, text_size

class Settings(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        #fps stuff
        self.fps_toggle = touchtrigger.Touchtrigger((0, 0), (256, 24))
        self.show_fps = False
        self.fps = fpscounter.Fpscounter()
        self.info_text = text.Text("loading", 24, (0, 0))
        #components
        self.title_textobject = text.Text("Settings", text_size["title"], (100, 100), colors["white"][0])
        self.back_buttonobject = button.Button("Back", 32, (64, global_vars.sys_screen_size[1]-128), (128, 64), UI_colors["danger"])
        #configure components
    
    def handle_event(self, event):
        if self.fps_toggle.update(event):
            self.show_fps = not self.show_fps
        if self.back_buttonobject.is_clicked(event):
            self.manager.switch_to_scene("Main menu")
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        if self.show_fps:
            self.info_text.set_text(f"FPS: {self.fps.get_fps()}, Mouse: X={pygame.mouse.get_pos()[0]} Y={pygame.mouse.get_pos()[1]}")
            self.info_text.draw(surface)
        self.title_textobject.draw(surface)
        self.back_buttonobject.draw(surface)
    
    def update(self):
        self.fps.tick()