import pygame, global_vars

class Touchtrigger:
    def __init__(self, location: tuple, size: tuple) -> None:
        self.location = location
        self.size = size
        self.font = pygame.font.Font(None, 24)

        #create rectangle for collision detection
        self.rect = pygame.Rect(self.location, self.size)

        #create surface for trigger (invisible)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.fill((255, 255, 255, 0))  #fully transparent

    def update(self, event): #event handler
        # check if event is mouse button RELEASE
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # 1 = left mouse button
            #check if mouse position is over rect
            if self.rect.collidepoint(global_vars.get_mouse_pos()):
                return True  #trigger activated
        return False

    def draw_debug(self, surface, name: str = ""):
        #draw outline for debugging
        surface.blit(self.surface, self.location)
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 3)
        name_surface = self.font.render(name, True, (255, 255, 255))  # White text
        surface.blit(name_surface, (self.location[0] + 3, self.location[1] + 3))