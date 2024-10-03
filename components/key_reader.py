import pygame

class KeyReader:
    def __init__(self):
        self.pressed_keys = set()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            #print("added:", pygame.key.name(event.key))
            self.pressed_keys.add(pygame.key.name(event.key))
        elif event.type == pygame.KEYUP:
            #print("removed:", pygame.key.name(event.key))
            try:
                self.pressed_keys.discard(pygame.key.name(event.key))
            except:
                pass

    def get_keys(self):
        return list(self.pressed_keys)