import pygame
class DisplayImage:
    def __init__(self, image_path: str, position: tuple, size: tuple) -> None:
        self.image = image_path
        self.size = size
        self.position = position
        self._render()

    def _render(self):
        try:
            self.img_obj = pygame.transform.smoothscale(pygame.image.load(self.image), self.size)
        except Exception as e: #draws missing texture (like in source engine or minecraft)
            print("Recoverable exception:", e)
            self.img_obj = pygame.Surface(self.size)
            pygame.draw.rect(self.img_obj, (255, 0, 255), pygame.Rect(0, 0, self.size[0]/2, self.size[1]/2))
            pygame.draw.rect(self.img_obj, (0, 0, 0), pygame.Rect(self.size[0]/2, 0, self.size[0]/2, self.size[1]/2))
            pygame.draw.rect(self.img_obj, (0, 0, 0), pygame.Rect(0, self.size[1]/2, self.size[0]/2, self.size[1]/2))
            pygame.draw.rect(self.img_obj, (255, 0, 255), pygame.Rect(self.size[0]/2, self.size[1]/2, self.size[0]/2, self.size[1]/2))
    
    def draw(self, surface):
        #blits the prerendered buffer to the given surface
        surface.blit(self.img_obj, self.position)
    
    def set_pos(self, new_pos:tuple):
        self.position = new_pos
    
    def get_pos(self):
        return self.position
    
    def set_image(self, new_image:str):
        self.image = new_image
        self._render()