import pygame, time

from elements import button, text, inputbox, touchtrigger

# Define colors
color_start = (93, 0, 133)  # RGB for #5d0085
color_end = (0, 0, 128)     # RGB for #000080

def draw_gradient(surface, color_start, color_end):
    for y in range(surface.get_height()):
        # Interpolate the color
        ratio = y / surface.get_height()
        r = int(color_start[0] * (1 - ratio) + color_end[0] * ratio)
        g = int(color_start[1] * (1 - ratio) + color_end[1] * ratio)
        b = int(color_start[2] * (1 - ratio) + color_end[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Editor")

def editor():
    frametime = time.time()
    framebucket = [0, 0, int(time.time())]
    testbutton = button.Button("click", (100, 100), 24, 300, 2)
    testtext = text.Text("0", 64, (500, 500))
    testinput = inputbox.InputBox(300, 32, (500, 300), 32)
    testtouchtrigger = touchtrigger.Touchtrigger((700, 700), (100, 100))
    while True:
        for event in pygame.event.get():  # Handle events
            testtouchtrigger.update(event)
            testinput.handle_event(event)
            if testbutton.is_clicked(event):
                testtext.set_text(str(int(testtext.get_text())+1))
            if event.type == pygame.QUIT:  # Check for quit event
                pygame.quit()
                return
        draw_gradient(screen, color_start, color_end)
        #screen.fill((0, 0, 0))
        testbutton.draw(screen)
        screen.blit(pygame.font.SysFont("Arial", 16).render(f"FPS: {framebucket[1]}, frame time: {time.time() - frametime} s", True, (255, 255, 255)), (4, 4))
        testtext.draw(screen)
        testinput.draw(screen)
        testtouchtrigger.draw_debug(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        frametime = time.time()
        if framebucket[2] < int(time.time()):
            framebucket[1] = framebucket[0]
            framebucket = [2, framebucket[1], int(time.time())]
        else:
            framebucket[0] += 1

editor()