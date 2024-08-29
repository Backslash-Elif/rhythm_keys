import pygame
class DisplayImage:
    def __init__(self, image_path: str, position: tuple, size: tuple) -> None:
        self.img_obj = pygame.transform.scale(pygame.image.load(image_path), size) #create image object
        self.position = position
    
    def draw(self, surface):
        #blits the prerendered buffer to the given surface
        surface.blit(self.img_obj, self.position)