import pygame, global_vars, tools
from scenes import scene

from components import button, text, touchtrigger, fpscounter, bgstyle
from components.styles import Styles

class EditorMainMenu(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        #fps stuff
        self.fps_toggle = touchtrigger.Touchtrigger((0, 0), (256, 24))
        self.show_fps = False
        self.fps = fpscounter.Fpscounter()
        self.info_text = text.Text("loading", 24, (0, 0))
        #components
        self.title_text = text.Text("Welcome to the editor!", 128, (0, 175), Styles.colors.light_green())
        self.create_button = button.Button("Create New", 32, tools.Screen.center_obj(global_vars.sys_screen_size, (512, 64), (0, -72)), (512, 64), Styles.button.primary())
        self.open_button = button.Button("Open...", 32, tools.Screen.center_obj(global_vars.sys_screen_size, (512, 64)), (512, 64), Styles.button.secondary())
        self.back_button = button.Button("Back", 32, tools.Screen.center_obj(global_vars.sys_screen_size, (512, 64), (0, 72)), (512, 64), Styles.button.secondary())
        #configure components
        self.title_text.set_position((tools.Screen.center_axis(global_vars.sys_screen_size[0], self.title_text.get_size()[0]), self.title_text.get_position()[1]))
    
    def handle_event(self, event):
        if self.fps_toggle.update(event):
            self.show_fps = not self.show_fps
        if self.create_button.is_clicked(event):
            self.manager.switch_to_scene("Editor create menu")
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, Styles.bggradient.purple())
        if self.show_fps:
            self.info_text.set_text(f"FPS: {self.fps.get_fps()}, Mouse: X={pygame.mouse.get_pos()[0]} Y={pygame.mouse.get_pos()[1]}")
            self.info_text.draw(surface)
        self.title_text.draw(surface)
        self.create_button.draw(surface)
        self.open_button.draw(surface)
        self.back_button.draw(surface)
    
    def update(self):
        self.fps.tick()