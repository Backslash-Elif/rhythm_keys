import scene, random

from elements import button, text, inputbox, touchtrigger, fpscounter, bgstyle
from elements.styles import Styles

class Editor(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        #fps stuff
        self.fps_toggle = touchtrigger.Touchtrigger((0, 0), (64, 24))
        self.show_fps = False
        self.fps = fpscounter.Fpscounter()
        self.fps_text = text.Text("loading", 24, (0, 0))
        #elements
        self.numberdisplay = text.Text(str(random.randint(1, 1000)), 64, (500, 500))
        self.refreshbutton = button.Button("Refresh", (500, 700), 32, 256, Styles.button.primary())
    
    def handle_event(self, event):
        if self.fps_toggle.update(event):
            self.show_fps = not self.show_fps
        if self.refreshbutton.is_clicked(event):
            self.manager.switch_to_scene("Editor")
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, Styles.bggradient.purple())
        if self.show_fps:
            self.fps_text.set_text(f"FPS: {self.fps.get_fps()}")
            self.fps_text.draw(surface)
        self.numberdisplay.draw(surface)
        self.refreshbutton.draw(surface)
    
    def update(self):
        self.fps.tick()