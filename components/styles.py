def compute_accent(original_color: tuple) -> tuple[tuple, tuple]: #calculates the lighter or darker accent of a color
    brightness = 0.299*original_color[0]/255 + 0.587*original_color[1]/255 + 0.114*original_color[2]/255 #0.299, 0.587, 0.114 perceived brightness of rgb
    
    difference = 20 #seems to be an universally good color difference
    if brightness >= 0.5:
        difference *= -1 #making negative for darkening
        text_color = (0, 0, 0)
    else:
        text_color = (255, 255, 255)
    
    return (original_color, (min(255, max(0, original_color[0]+difference)), min(255, max(0, original_color[1]+difference)), min(255, max(0, original_color[2]+difference))), text_color) #returns both original and accent and text color

colors = { #standard colors in format (R, G, B)
    "red": (255, 0, 0),
    "light_red": (255, 99, 71),
    "dark_red": (139, 0, 0),
    "green": (0, 255, 0),
    "light_green": (0, 255, 127),
    "darkgreen": (0, 100, 0),
    "blue": (0, 0, 255),
    "light_blue": (11, 87, 208),
    "dark_blue": (0, 0, 128),
    "purple": (132, 3, 252),
    "pink": (255, 20, 147),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0),
    "gray": (128, 128, 128),
    "light_gray": (200, 200, 200),
    "dark_gray": (64, 64, 64),
    "black_gray": (33, 33, 33),
    "white": (255, 255, 255),
    "black": (0, 0, 0)
}

themed_colors = {} #pre-calculated accented colors in format ((standard color), (accented color), (text color))
for key, value in colors.items():
    themed_colors[key] = compute_accent(value)

UI_colors = {} #primary, secondary, attention, danger, success

background_gradient = {#((bgcolor-start), (bgcolor-end), dark_color:bool)
    "midnight": (colors["blue"], colors["dark_blue"], True),
    "daybreak": (colors["orange"], colors["purple"], False),
    "Cotton_candy": (colors["pink"], colors["purple", False]),
    "grassy_hill": (colors["light_green"], colors["green"], False),
    "ocean": (colors["light_blue"], colors["blue"], False),
    "coral_reef": (colors["red"], colors["blue"], True)
}

card_themes = { #(R, G, B, A)
    "light": colors["white"]+(64, ),
    "dark": colors["black"]+(64, ),
    "primary": colors["light_blue"]+(64, ),
    "attention": colors["yellow"]+(64, ),
}

class Styles:
    class button:
        #color, hover color, text color
        @staticmethod
        def primary():
            return ((11, 87, 208), compute_accent((11, 87, 208), True), (255, 255, 255))
        
        @staticmethod
        def secondary():
            return ((33, 33, 33), compute_accent((33, 33, 33), True), (255, 255, 255))
        
        @staticmethod
        def danger():
            return ((255, 0, 0), compute_accent((255, 0, 0)), (255, 255, 255))
        
        @staticmethod
        def blue():
            return ((0, 142, 254), compute_accent((0, 142, 254)), (255, 255, 255))
        
        @staticmethod
        def green():
            return ((0, 255, 127), compute_accent((0, 255, 127)), (0, 0, 0))
    
    class inputbox:
        #color, active color, text color
        @staticmethod
        def light():
            return ((200, 200, 200), compute_accent((200, 200, 200)), (0, 0, 0))
        
        @staticmethod
        def dark():
            return ((33, 33, 33), compute_accent((33, 33, 33), True), (255, 255, 255))
    
    class bggradient:
        #start color, end color
        @staticmethod
        def purple():
            return ((93, 0, 133), (0, 0, 128))

    class card:
        #srgb
        @staticmethod
        def light():
            return (255, 255, 255, 64)
        
        @staticmethod
        def dark():
            return (0, 0, 0, 64)
        
        @staticmethod
        def primary():
            return(11, 87, 208, 64)
        
        @staticmethod
        def attention():
            return(255, 255, 0, 64)
        
        @staticmethod
        def danger():
            return(255, 0, 0, 64)
    
    class colors:
        #red, green, blue
        @staticmethod
        def red():
            return (255, 0, 0)
        
        @staticmethod
        def light_red():
            return (255, 99, 71)
        
        @staticmethod
        def green():
            return (0, 255, 0)
        
        @staticmethod
        def light_green():
            return (0, 255, 127)
        
        @staticmethod
        def blue():
            return (0, 0, 255)
        
        @staticmethod
        def light_blue():
            return (11, 87, 208)
        
        @staticmethod
        def purple():
            return (132, 3, 252)
        
        @staticmethod
        def magenta():
            return (255, 0, 255)
        
        @staticmethod
        def orange():
            return (255, 165, 0)
        
        @staticmethod
        def yellow():
            return (255, 255, 0)
        
        @staticmethod
        def gray():
            return (128, 128, 128)
        
        @staticmethod
        def light_gray():
            return (200, 200, 200)
        
        @staticmethod
        def dark_gray():
            return (64, 64, 64)
        
        @staticmethod
        def black_gray():
            return (33, 33, 33)
        
        @staticmethod
        def white():
            return (255, 255, 255)
        
        @staticmethod
        def black():
            return (0, 0, 0)
    
    class textsize:
        @staticmethod
        def large_title():
            return 128
        
        @staticmethod
        def title():
            return 96
        
        @staticmethod
        def small_title():
            return 64
        
        @staticmethod
        def subtitle():
            return 48
        
        @staticmethod
        def text():
            return 32
        
        @staticmethod
        def small_text():
            return 24