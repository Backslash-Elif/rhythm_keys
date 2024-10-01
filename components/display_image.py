import pygame
class DisplayImage:
    def __init__(self, image_path: str, position: tuple, size: tuple) -> None:
        self.image = image_path
        self.size = size
        self.position = position
        self._render()

    def _render(self):
        try:
            self.img_obj = pygame.transform.scale(pygame.image.load(self.image), self.size)
        except: #draws missing texture (like in source engine or minecraft)
            self.img_obj = pygame.Surface(self.size)
            self.rect1 = pygame.Rect(0, 0, self.size[0]/2, self.size[1]/2)
            self.rect2 = pygame.Rect(self.size[0]/2, 0, self.size[0]/2, self.size[1]/2)
            self.rect3 = pygame.Rect(0, self.size[1]/2, self.size[0]/2, self.size[1]/2)
            self.rect4 = pygame.Rect(self.size[0]/2, self.size[1]/2, self.size[0]/2, self.size[1]/2)
            pygame.draw.rect(self.img_obj, (255, 0, 255), self.rect1)
            pygame.draw.rect(self.img_obj, (0, 0, 0), self.rect2)
            pygame.draw.rect(self.img_obj, (0, 0, 0), self.rect3)
            pygame.draw.rect(self.img_obj, (255, 0, 255), self.rect4)
    
    def draw(self, surface):
        #blits the prerendered buffer to the given surface
        surface.blit(self.img_obj, self.position)
    
    def set_pos(self, new_pos:tuple):
        self.position = new_pos
    
    def set_image(self, new_image:str):
        self.image = new_image
        self._render()