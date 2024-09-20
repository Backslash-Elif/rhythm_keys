import pygame, global_vars, tools
from scenes import scene

from components import button, text, touchtrigger, fpscounter, bgstyle, inputbox
from components.styles import colors, UI_colors, background_gradient, text_size, compute_dynamic_colors

class OutOfBoxExperience(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        #fps stuff
        self.fps_toggle = touchtrigger.Touchtrigger((0, 0), (256, 24))
        self.show_fps = False
        self.fps = fpscounter.Fpscounter()
        self.info_text = text.Text("loading", 24, (0, 0))
        #components
        self.title_textobject = text.Text("Welcome to rhythm keys!", text_size["title"], (100, 100), colors["black"][0])
        self.subtitle_textobject = text.Text("Tell us a bit about yourself", text_size["subtitle"], (100, 200), colors["black"][0])
        self.username_textobject = text.Text("Username", text_size["text"], (100, 280), colors["gray"][0])
        self.username_inputobject = inputbox.InputBox((500, 50), text_size["subtitle"], (100, 300), 16, UI_colors["secondary"])
        self.darkmode_buttonobject = button.Button("Switch to dark mode", text_size["text"], (100, 500), (50, 200), UI_colors["secondary"])
    
    def handle_event(self, event):
        if self.fps_toggle.update(event):
            self.show_fps = not self.show_fps
        self.username_inputobject.handle_events(event)
        if self.darkmode_buttonobject.is_clicked(event):
            global_vars.user_dark_mode = not global_vars.user_dark_mode
            compute_dynamic_colors()
            
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        if self.show_fps:
            self.info_text.set_text(f"FPS: {self.fps.get_fps()}, Mouse: X={pygame.mouse.get_pos()[0]} Y={pygame.mouse.get_pos()[1]}")
            self.info_text.draw(surface)
        self.title_textobject.draw(surface)
        self.subtitle_textobject.draw(surface)
        self.username_textobject.draw(surface)
        self.username_inputobject.draw(surface)
        self.darkmode_buttonobject.draw(surface)
    
    def update(self):
        self.fps.tick()