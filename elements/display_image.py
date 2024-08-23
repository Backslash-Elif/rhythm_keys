import pygame
class DisplayImage:
    def __init__(self, image_path: str, location: tuple, size: tuple) -> None:
        self.img_obj = pygame.transform.scale(pygame.image.load(image_path), size)
        self.location = location
    
    def draw(self, surface):
        surface.blit(self.img_obj, self.location)