class Styles:
    class button:
        #color, hover color, text color
        @staticmethod
        def primary():
            return ((11, 87, 208), (30, 100, 212), (255, 255, 255))
        
        @staticmethod
        def secondary():
            return ((33, 33, 33), (43, 43, 43), (255, 255, 255))
        
        @staticmethod
        def danger():
            return ((255, 0, 0), (204, 0, 0), (255, 255, 255))
    
    class inputbox:
        #color, active color, text color
        @staticmethod
        def light():
            return ((200, 200, 200), (170, 170, 170), (0, 0, 0))
        
        @staticmethod
        def dark():
            return ((33, 33, 33), (43, 43, 43), (255, 255, 255))
    
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