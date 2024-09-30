import pygame, global_vars, scene_manager

class ScreenManager:
    def __init__(self) -> None:
        self.screensize_id = global_vars.sys_screen_size_id
        self.screensizes = ((1280, 720), (1920, 1080), (2560, 1440), (3840, 2160))
        self.current_screensize = self.screensizes[self.screensize_id]
        self.virtual_screen = pygame.Surface((1920, 1080)) #native screensize
        self.screen = pygame.display.set_mode(self.current_screensize)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Rhythm Keys")

        self.scene_mgr = scene_manager.SceneManager(self, "Main menu")
    
    def handle_event(self, event):

        self.scene_mgr.handle_event(event)

    def draw(self):
        self.scene_mgr.draw(self.virtual_screen)
        self.screen.blit(pygame.transform.scale(self.virtual_screen, self.current_screensize), (0, 0))
    
    def flip_screen(self):
        pygame.display.flip()
    
    def tick(self, framerate):
        self.clock.tick(framerate)
    
    def set_screensize(self, screensize_id: int):
        self.screensize_id = screensize_id
        self.current_screensize = self.screensizes[self.screensize_id]
        global_vars.sys_screen_size_id = screensize_id
        global_vars.sys_current_screen_size = self.current_screensize
        self.screen = pygame.display.set_mode(self.current_screensize)