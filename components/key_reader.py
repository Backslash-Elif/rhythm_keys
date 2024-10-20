import pygame

class KeyReader:
    def __init__(self):
        self.pressed_keys = set()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN: #adds keys to set
            self.pressed_keys.add(pygame.key.name(event.key))
        elif event.type == pygame.KEYUP: #removes keys from set
            try:
                self.pressed_keys.discard(pygame.key.name(event.key))
            except Exception as e:
                print("Recoverable exception:", e)

    def get_keys(self):
        return list(self.pressed_keys)
    
    def get_pressed_key(self, event): #shortcut for getting newly pressed down keys
        if event.type == pygame.KEYDOWN:
            return pygame.key.name(event.key)
    
    def get_released_key(self, event):#shortcut for getting newly released keys
        if event.type == pygame.KEYUP:
            return pygame.key.name(event.key)