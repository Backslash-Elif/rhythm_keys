class Tools:
    class screen:
        def findcenterwithobject(screensize: tuple, objectsize: tuple, shift: tuple = (0, 0)):
            x_cor = (screensize[0]/2) - (objectsize[0]/2) + shift[0]
            y_cor = (screensize[1]/2) - (objectsize[1]/2) + shift[1]
            return (x_cor, y_cor)