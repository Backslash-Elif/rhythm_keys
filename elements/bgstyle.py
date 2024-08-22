import pygame

class Bgstyle:
    def __init__(self) -> None:
        pass
    
    def gradient(surface, color_start, color_end)
        for y in range(surface.get_height()):
            # Interpolate the color
            ratio = y / surface.get_height()
            r = int(color_start[0] * (1 - ratio) + color_end[0] * ratio)
            g = int(color_start[1] * (1 - ratio) + color_end[1] * ratio)
            b = int(color_start[2] * (1 - ratio) + color_end[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))