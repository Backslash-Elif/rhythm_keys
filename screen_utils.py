def center_axis(surface_size: int, object_size: int, shift: int = 0): #returns the centered x cordinates
    centered_axis = (surface_size/2) - (object_size/2) + shift
    return centered_axis
    
def center_obj(surface_size: tuple, object_size: tuple, shift: tuple = (0, 0)): #returns the centered cordinates
    x_cor = center_axis(surface_size[0], object_size[0], shift[0])
    y_cor = center_axis(surface_size[1], object_size[1], shift[1])
    return (x_cor, y_cor)