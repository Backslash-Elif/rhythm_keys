import pygame

class Bgstyle:
    def __init__(self) -> None:
        pass
    
    def draw_gradient(surface, colors: tuple):
        color_start, color_end = colors
        for y in range(surface.get_height()):
            # Interpolate the color
            ratio = y / surface.get_height()
            r = int(color_start[0] * (1 - ratio) + color_end[0] * ratio)
            g = int(color_start[1] * (1 - ratio) + color_end[1] * ratio)
            b = int(color_start[2] * (1 - ratio) + color_end[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))
    
    def draw_color(surface, color: tuple):
        surface.fill(color)