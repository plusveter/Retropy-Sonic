from .datamask import DataMask
import pygame as pg
import numpy as np


#-[ NOTE ]-------------------------------------------------------------------------------
# This is a bunch of code i made, takken from the last version of the previous iterations
#----------------------------------------------------------------------------------------

# Setup the mask side
def point_to_dmask(point:list[int], position:list[int]) -> DataMask:
    """
    **Make DataMask using a point**         (also know as sensor_point)
    >>> rect_to_dmask([offsetx, offsety], [parentx, parenty])
    """
    mask = pg.mask.from_surface(pg.Surface((1, 1)))
    return DataMask(mask, np.array([int(position[0]), int(position[1]), int(point[0]), int(point[1]), 1, 1], dtype=np.int64))

def rect_to_dmask(rect:list[int], position:list[int]) -> DataMask:
    """
    **Make DataMask using a rectangle**    (also know as sensor_rect)
        >>> rect_to_dmask([offsetx, offsety, width, height], [parentx, parenty])
    """
    mask = pg.mask.from_surface(pg.Surface((rect[2], rect[3])))
    return DataMask(mask,  np.array([int(position[0]), int(position[1]), int(rect[0]), int(rect[1]), rect[2], rect[3]], dtype=np.int64))

def surface_to_dmask(surface:pg.Surface, position:list[int]) -> DataMask:
    """
    **Make DataMask using a surface**      (also know as solid_block)
        >>> rect_to_dmask(pygame.Surface, [parentx, parenty])
    """

    mask = pg.mask.from_surface(surface)
    width, height = surface.get_size()
    return DataMask(mask, np.array([int(position[0]), int(position[1]), 0, 0, width, height], dtype=np.int64))
