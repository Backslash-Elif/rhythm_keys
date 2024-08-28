import pygame, scene

from components import button, text, touchtrigger, fpscounter, bgstyle
from components.styles import Styles
from tools import Tools

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
        self.menucreate = button.Button("Create New", 32, Tools.screen.findcenterwithobject((1920, 1080), (512, 64), (0, -72)), 512, 64, Styles.button.primary())
        self.menuopen = button.Button("Open...", 32, Tools.screen.findcenterwithobject((1920, 1080), (512, 64)), 512, 64, Styles.button.secondary())
        self.menuback = button.Button("Back", 32, Tools.screen.findcenterwithobject((1920, 1080), (512, 64), (0, 72)), 512, 64, Styles.button.secondary())
    
    def handle_event(self, event):
        if self.fps_toggle.update(event):
            self.show_fps = not self.show_fps
        if self.menucreate.is_clicked(event):
            self.manager.switch_to_scene("Editor create menu")
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, Styles.bggradient.purple())
        if self.show_fps:
            self.info_text.set_text(f"FPS: {self.fps.get_fps()}, Mouse: X={pygame.mouse.get_pos()[0]} Y={pygame.mouse.get_pos()[1]}")
            self.info_text.draw(surface)
        self.menucreate.draw(surface)
        self.menuopen.draw(surface)
        self.menuback.draw(surface)
    
    def update(self):
        self.fps.tick()