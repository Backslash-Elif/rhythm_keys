def compute_accent(original_color: tuple, lighten:bool=False): #calculates the x% lighter or darker accent of a color
    percentage = 15 #%
    difference_factor = 100/percentage
    difference = (original_color[0]/difference_factor, original_color[1]/difference_factor, original_color[2]/difference_factor)
    if lighten:
        return (int(original_color[0]+difference[0]), int(original_color[1]+difference[1]), int(original_color[2]+difference[2])) #returns color with lighter accent
    else:
        return (int(original_color[0]-difference[0]), int(original_color[1]-difference[1]), int(original_color[2]-difference[2])) #returns color with darker accent

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