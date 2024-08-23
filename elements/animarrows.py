import pygame, os

class Animarrowstriggerbar:
    def __init__(self) -> None:
        self.arrow_images = {
            'up': pygame.transform.scale(pygame.image.load(os.path.join('assets/arrows/smol_dark', 'up.png')), (64, 64)),
            'down': pygame.transform.scale(pygame.image.load(os.path.join('assets/arrows/smol_dark', 'down.png')), (64, 64)),
            'left': pygame.transform.scale(pygame.image.load(os.path.join('assets/arrows/smol_dark', 'left.png')), (64, 64)),
            'right': pygame.transform.scale(pygame.image.load(os.path.join('assets/arrows/smol_dark', 'right.png')), (64, 64))
        }