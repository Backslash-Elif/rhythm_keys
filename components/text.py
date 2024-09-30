import pygame, tools
from enum import Enum

class TextAlign(Enum):
    TOP_LEFT = "top left"
    TOP = "top"
    TOP_RIGHT = "top right"
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    BOTTOM_LEFT = "bottom left"
    BOTTOM = "bottom"
    BOTTOM_RIGHT = "bottom right"

class Text:
    def __init__(self, text: str, text_size: int, position: tuple, size: tuple, color:tuple = (255, 255, 255), text_align: TextAlign = TextAlign.CENTER) -> None:
        self.display_text = text
        self.text_size = text_size
        self.position = position
        self.text_color = color
        self.text_align = text_align
        self.size = size

        self.font = pygame.font.SysFont(None, self.text_size) #font set to None for pygame built-in font
        self._render()
    
    def _render(self):
        self.buffer = pygame.Surface(self.size, pygame.SRCALPHA)
        textsegments, segment_heights, total_size = self.__compute_newlines(self.display_text)
        text_position = (0, 0)
        if self.text_align == TextAlign.TOP_LEFT:
            text_position = (0, 0)
        elif self.text_align == TextAlign.TOP:
            text_position = (tools.Screen.center_axis(self.size[0], total_size[0]), 0)
        elif self.text_align == TextAlign.TOP_RIGHT:
            text_position = (self.size[0] - total_size[0], 0)
        elif self.text_align == TextAlign.LEFT:
            text_position = (0, tools.Screen.center_axis(self.size[1], total_size[1]))
        elif self.text_align == TextAlign.CENTER:
            text_position = (tools.Screen.center_obj(self.size, total_size))
        elif self.text_align == TextAlign.RIGHT:
            text_position = (self.size[0] - total_size[0], tools.Screen.center_axis(self.size[1], total_size[1]))
        elif self.text_align == TextAlign.BOTTOM_LEFT:
            text_position = (0, self.size[1] - total_size[1])
        elif self.text_align == TextAlign.BOTTOM:
            text_position = (tools.Screen.center_axis(self.size[0], total_size[0]), self.size[1] - total_size[1])
        elif self.text_align == TextAlign.BOTTOM_RIGHT:
            text_position = (self.size[0] - total_size[0], self.size[1] - total_size[1])
        
        for segment, height_index in zip(textsegments, range(len(segment_heights))):
            text_surface = self.font.render(segment, True, self.text_color)
            self.buffer.blit(text_surface, (text_position[0], text_position[1]+sum(segment_heights[0:height_index])))
    
    def __compute_newlines(self, inputtext: str): #internal method for getting text segments, their height and their complete size
        inputtext = inputtext.replace("\n\n", "\n \n")
        segments = inputtext.split("\n")
        widths = []
        heights = []
        for segment in segments:
            tempsize = self.font.size(segment)
            widths.append(tempsize[0])
            heights.append(tempsize[1])
        return segments, heights, (max(widths), sum(heights)) #textsegments, segment height, (total width, total height)
    
    def draw(self, surface): #draw to surface
        surface.blit(self.buffer, self.position)
    
    def get_size(self): #gets the size of the text
        return self.size
    
    def set_size(self, new_size: tuple): #gets the size of the text
        self.size = new_size
        self._render()
    
    def get_text(self): #getter method text
        return self.display_text
    
    def set_text(self, newtext:str): #setter method text
        self.display_text = newtext
        self._render()
    
    def get_position(self): #getter method text position
        return self.position
    
    def set_position(self, newposition: tuple): #setter method text position
        self.position = newposition