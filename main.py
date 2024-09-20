import pygame, scene_manager

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Rhythm Keys")
clock = pygame.time.Clock()

scene_mgr = scene_manager.SceneManager("Main menu")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        scene_mgr.handle_event(event)
    
    scene_mgr.update()
    scene_mgr.draw(screen)
    pygame.display.flip()
    clock.tick(60)