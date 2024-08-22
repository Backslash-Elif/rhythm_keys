class Styles:
    class button:
        #color, hover color
        @staticmethod
        def primary():
            return [(11, 87, 208), (30, 100, 212)]
        
        @staticmethod
        def secondary():
            return [(33, 33, 33), (43, 43, 43)]
        
        @staticmethod
        def danger():
            return [(255, 0, 0), (204, 0, 0)]
    
    class inputbox:
        #color, active color, text color
        @staticmethod
        def light():
            return [(200, 200, 200), (170, 170, 170), (0, 0, 0)]
        
        @staticmethod
        def dark():
            return [(33, 33, 33), (43, 43, 43), (255, 255, 255)]