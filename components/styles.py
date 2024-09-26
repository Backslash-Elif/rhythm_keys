import global_vars
from enum import Enum

#color manipulation
def get_color_brightness(color: tuple):
    r, g, b = color
    return 0.299*color[0]/255 + 0.587*color[1]/255 + 0.114*color[2]/255 #0.299, 0.587, 0.114 perceived brightness of rgb

def change_color(color: tuple, difference: int):
    r, g, b = color
    return (min(255, max(0, r + difference)), min(255, max(0, g + difference)), min(255, max(0, b + difference))) #returns the changed color as tuple

def compute_accent(original_color: tuple) -> tuple[tuple, tuple, tuple]: #calculates the lighter or darker accent of a color
    brightness = get_color_brightness(original_color)
    
    difference = 20 #seems to be an universally good color difference
    if brightness >= 0.5:
        difference *= -1 #making negative for darkening
        text_color = (0, 0, 0)
    else:
        text_color = (255, 255, 255)
    #print(original_color, change_color(original_color, difference), text_color)
    return (original_color, change_color(original_color, difference), text_color) #returns both original and accent and text color

def compute_bg(start_color: tuple, end_color:tuple): #custom function to calculate darker color for bg
    change_value = 255 - max(start_color + end_color)
    if change_value > 0:
        start_color = change_color(start_color, change_value)
        end_color = change_color(end_color, change_value)
    brightness = 100 if global_vars.user_dark_mode else 200
    brightness /= 255
    return ((int(start_color[0]*brightness), int(start_color[1]*brightness), int(start_color[2]*brightness)), (int(end_color[0]*brightness), int(end_color[1]*brightness), int(end_color[2]*brightness)))

#enums
class ColorName(Enum):
    RED = "red"
    LIGHT_RED = "light_red"
    SOFT_RED = "soft_red"
    DARK_RED = "dark_red"
    GREEN = "green"
    LIGHT_GREEN = "light_green"
    DARK_GREEN = "dark_green"
    BLUE = "blue"
    LIGHT_BLUE = "light_blue"
    DARK_BLUE = "dark_blue"
    SKY_BLUE = "sky_blue"
    PURPLE = "purple"
    PINK = "pink"
    MAGENTA = "magenta"
    ORANGE = "orange"
    YELLOW = "yellow"
    GRAY = "gray"
    LIGHT_GRAY = "light_gray"
    DARK_GRAY = "dark_gray"
    BLACK_GRAY = "black_gray"
    WHITE = "white"
    BLACK = "black"
    DYNAMIC = "dynamic"

class UIColorName(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"

class BGGradientName(Enum):
    MIDNIGHT = "midnight"
    DAYBREAK = "daybreak"
    ORCHIDS = "orchids"
    PEPPERMINT = "peppermint"
    FORREST = "forrest"
    AUTUMN = "autumn"
    OCEAN = "ocean"
    MOUNTAIN_MIST = "mountain_mist"
    CHERRY_BLOSSOM = "cherry_blossom"
    NONE = "none"

class CardThemeName(Enum):
    LIGHT = "light"
    DARK = "dark"
    PRIMARY = "primary"
    WARNING = "warning"
    DANGER = "danger"
    DYNAMIC = "dynamic"

class TextSizeName(Enum):
    LARGE_TITLE = "large_title"
    TITLE = "title"
    SMALL_TITLE = "small_title"
    SUBTITLE = "subtitle"
    TEXT = "text"
    SMALL_TEXT = "small_text"

colors = { #original colors in format (R, G, B)
    ColorName.RED: (255, 0, 0),
    ColorName.LIGHT_RED: (255, 99, 71),
    ColorName.SOFT_RED: (225, 18, 69),
    ColorName.DARK_RED: (139, 0, 0),
    ColorName.GREEN: (0, 255, 0),
    ColorName.LIGHT_GREEN: (0, 255, 127),
    ColorName.DARK_GREEN: (0, 100, 0),
    ColorName.BLUE: (0, 0, 255),
    ColorName.LIGHT_BLUE: (11, 87, 208),
    ColorName.DARK_BLUE: (0, 0, 128),
    ColorName.SKY_BLUE: (0, 191, 255),
    ColorName.PURPLE: (132, 3, 252),
    ColorName.PINK: (255, 20, 147),
    ColorName.MAGENTA: (255, 0, 255),
    ColorName.ORANGE: (255, 165, 0),
    ColorName.YELLOW: (255, 255, 0),
    ColorName.GRAY: (128, 128, 128),
    ColorName.LIGHT_GRAY: (212, 212, 212),
    ColorName.DARK_GRAY: (58, 58, 58),
    ColorName.BLACK_GRAY: (33, 33, 33),
    ColorName.WHITE: (255, 255, 255),
    ColorName.BLACK: (0, 0, 0)
}

#pre-calculates auto-generated accented colors and their matching text-color, done to reduce redundant color calculations. in format {key, ((standard color), (accented color), (text color))}
for key, value in colors.items():
    colors[key] = compute_accent(value)
colors[ColorName.DYNAMIC] = ((0, 0, 0), (58, 58, 58), (255, 255, 255)) #init fir dynamic color

UI_colors = {} #unified shortcuts to various colors which are used for the UI
background_gradient = {}
card_themes = {} #(R, G, B, A)

def compute_dynamic_colors():
    colors[ColorName.DYNAMIC] = ((255, 255, 255), (212, 212, 212), (0, 0, 0)) if global_vars.user_dark_mode else ((0, 0, 0), (58, 58, 58), (255, 255, 255))

    UI_colors[UIColorName.PRIMARY] = ((0, 111, 238), (0, 100, 214), (255, 255, 255)) if global_vars.user_dark_mode else ((0, 111, 238), (51, 140, 241), (255, 255, 255))
    UI_colors[UIColorName.SECONDARY] = ((63, 63, 70), (57, 57, 63), (255, 255, 255)) if global_vars.user_dark_mode else ((212, 212, 216), (221, 221, 224), (0, 0, 0))
    UI_colors[UIColorName.SUCCESS] = ((23, 201, 100), (21, 181, 90), (0, 0, 0)) if global_vars.user_dark_mode else ((23, 201, 100), (69, 212, 131), (0, 0, 0))
    UI_colors[UIColorName.WARNING] = ((245, 165, 36), (220, 148, 32), (0, 0, 0)) if global_vars.user_dark_mode else ((245, 165, 36), (247, 183, 80), (0, 0, 0))
    UI_colors[UIColorName.DANGER] = ((243, 18, 96), (219, 16, 86), (255, 255, 255)) if global_vars.user_dark_mode else ((243, 18, 96), (245, 65, 128), (255, 255, 255))
    
    background_gradient[BGGradientName.MIDNIGHT.value] = (compute_bg(colors[ColorName.DARK_BLUE][0], colors[ColorName.PURPLE][0])) #darkblue, purple
    background_gradient[BGGradientName.DAYBREAK.value] = (compute_bg(colors[ColorName.PURPLE][0], colors[ColorName.ORANGE][0]))
    background_gradient[BGGradientName.ORCHIDS.value] = (compute_bg(colors[ColorName.PINK][0], colors[ColorName.PURPLE][0]))
    background_gradient[BGGradientName.PEPPERMINT.value] = (compute_bg(colors[ColorName.SKY_BLUE][0], colors[ColorName.LIGHT_GREEN][0]))
    background_gradient[BGGradientName.FORREST.value] = (compute_bg(colors[ColorName.DARK_GREEN][0], colors[ColorName.LIGHT_GREEN][0]))
    background_gradient[BGGradientName.AUTUMN.value] = (compute_bg(colors[ColorName.ORANGE][0], colors[ColorName.RED][0]))
    background_gradient[BGGradientName.OCEAN.value] = (compute_bg(colors[ColorName.SKY_BLUE][0], colors[ColorName.BLUE][0]))
    background_gradient[BGGradientName.MOUNTAIN_MIST.value] = (compute_bg(colors[ColorName.DARK_BLUE][0], colors[ColorName.LIGHT_GRAY][0]))
    background_gradient[BGGradientName.CHERRY_BLOSSOM.value] = (compute_bg(colors[ColorName.SOFT_RED][0], colors[ColorName.WHITE][0]))
    background_gradient[BGGradientName.NONE.value] = (colors[ColorName.WHITE][0], colors[ColorName.WHITE][0]) if global_vars.user_dark_mode == False else (colors[ColorName.BLACK_GRAY][0], colors[ColorName.BLACK_GRAY][0])

    card_themes[CardThemeName.LIGHT] = colors[ColorName.WHITE][0]+(150, )
    card_themes[CardThemeName.DARK] = colors[ColorName.BLACK][0]+(100, )
    card_themes[CardThemeName.PRIMARY] = colors[ColorName.LIGHT_BLUE][0]+(100, )
    card_themes[CardThemeName.WARNING] = colors[ColorName.YELLOW][0]+(100, )
    card_themes[CardThemeName.DANGER] = colors[ColorName.RED][0]+(100, )
    card_themes[CardThemeName.DYNAMIC] = colors[ColorName.BLACK][0]+(100, ) if global_vars.user_dark_mode else colors[ColorName.WHITE][0]+(150, )

compute_dynamic_colors()

text_size = {
    TextSizeName.LARGE_TITLE: 128,
    TextSizeName.TITLE: 96,
    TextSizeName.SMALL_TITLE: 64,
    TextSizeName.SUBTITLE: 48,
    TextSizeName.TEXT: 32,
    TextSizeName.SMALL_TEXT: 24
}