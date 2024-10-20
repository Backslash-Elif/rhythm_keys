import pygame, global_vars
from scenes import main_menu, settings, oobe, editor_main_menu, editor_create_menu, editor_editor, level_selector, data_manager, main_game, results

class SceneManager:
    def __init__(self, screen_mgr, initial_scene: str) -> None:
        self.screen_mgr = screen_mgr
        self.scenes = {
            "Main menu": main_menu.MainMenu,
            "Settings": settings.Settings,
            "OOBE": oobe.OutOfBoxExperience,
            "Editor main menu": editor_main_menu.EditorMainMenu, 
            "Editor create menu": editor_create_menu.EditorCreateMenu,
            "Editor": editor_editor.EditorEditor,
            "Level selector": level_selector.LevelSelector,
            "Data manager": data_manager.DataManager,
            "Game": main_game.MainGame,
            "Level results": results.Results
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
    
    def set_screensize(self, screensize_id: int):
        self.screen_mgr.set_screensize(screensize_id)