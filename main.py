import pygame, scene_manager, global_vars

def get_screensize():
    return global_vars.const_screen_sizes[global_vars.sys_screen_size]

# Initialize Pygame
pygame.init()
screensize = get_screensize()
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption("Rhythm Keys")
clock = pygame.time.Clock()

scene_mgr = scene_manager.SceneManager("Main menu")

while True:
    if get_screensize() != screensize:
        screensize = get_screensize()
        scene_mgr.update_main_screen_size(screensize)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        scene_mgr.handle_event(event)
    
    scene_mgr.update()
    scene_mgr.draw(screen)
    pygame.display.flip()
    clock.tick(60)