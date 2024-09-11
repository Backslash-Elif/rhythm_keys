import pygame, tools
from scenes import scene

from components import fpscounter, touchtrigger, text, bgstyle
from components.styles import Styles

class EditorEditor(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager

        #fps stuff
        self.fps_toggle = touchtrigger.Touchtrigger((0, 0), (256, 24))
        self.show_fps = False
        self.fps = fpscounter.Fpscounter()
        self.info_text = text.Text("loading", 24, (0, 0))

        #text
        self.title_textobject = text.Text("Title", 64, (1100, 100))

    def handle_event(self, event):
        if self.fps_toggle.update(event):
            self.show_fps = not self.show_fps

    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, Styles.bggradient.purple())
        if self.show_fps:
            self.info_text.set_text(f"FPS: {self.fps.get_fps()}, Mouse: X={pygame.mouse.get_pos()[0]} Y={pygame.mouse.get_pos()[1]}")
            self.info_text.draw(surface)
        self.title_textobject.draw(surface)

    def update(self):
        self.fps.tick()