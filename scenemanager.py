from editor import Editor

class Scenemanager:
    def __init__(self, initial_scene: str) -> None:
        self.scenes = {
            "Editor": Editor
            }
        self.current_scene = self.scenes[initial_scene](self) #create a instance of the selected class
    
    def switch_to_scene(self, scenename):
        self.current_scene = None #gython garbage collection optimization, better than del
        self.current_scene = self.scenes[scenename](self)
    
    def handle_event(self, event):
        self.current_scene.handle_event(event)
    
    def draw(self, surface):
        self.current_scene.draw(surface)
    
    def update(self):
        self.current_scene.update()