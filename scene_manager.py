from scenes import main_menu, settings, oobe, editor_main_menu, editor_create_menu, editor_editor

class SceneManager:
    def __init__(self, initial_scene: str) -> None:
        self.scenes = {
            "Main menu": main_menu.MainMenu,
            "Settings": settings.Settings,
            "OOBE": oobe.OutOfBoxExperience,
            "Editor main menu": editor_main_menu.EditorMainMenu, 
            "Editor create menu": editor_create_menu.EditorCreateMenu,
            "Editor": editor_editor.EditorEditor
            }
        self.current_scene = self.scenes[initial_scene](self) #create a instance of the selected class
    
    def switch_to_scene(self, scenename):
        print("switching to scene ID: " + str(scenename))
        self.current_scene = None #gython garbage collection optimization, better than del
        self.current_scene = self.scenes[scenename](self)
    
    def handle_event(self, event):
        self.current_scene.handle_event(event)
    
    def draw(self, surface):
        self.current_scene.draw(surface)
    
    def update(self):
        self.current_scene.update()