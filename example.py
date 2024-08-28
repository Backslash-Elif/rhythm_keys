import scene, random

from components import button, text, touchtrigger, fpscounter, bgstyle
from components.styles import Styles

class Example(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        #fps stuff
        self.fps_toggle = touchtrigger.Touchtrigger((0, 0), (64, 24))
        self.show_fps = False
        self.fps = fpscounter.Fpscounter()
        self.fps_text = text.Text("loading", 24, (0, 0))
        #components
        self.numberdisplay = text.Text(str(random.randint(1, 1000)), 64, (500, 500))
        self.refreshbutton = button.Button("Refresh", 32, (500, 700), 256, 64, Styles.button.primary())
    
    def handle_event(self, event):
        if self.fps_toggle.update(event):
            self.show_fps = not self.show_fps
        if self.refreshbutton.is_clicked(event):
            self.manager.switch_to_scene("Example")
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, Styles.bggradient.purple())
        if self.show_fps:
            self.fps_text.set_text(f"FPS: {self.fps.get_fps()}")
            self.fps_text.draw(surface)
        self.numberdisplay.draw(surface)
        self.refreshbutton.draw(surface)
        self.fps_toggle.draw_debug(surface, "fps")
    
    def update(self):
        self.fps.tick()