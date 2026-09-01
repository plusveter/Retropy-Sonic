from .rectbox import RectBox
from .datamask import DataMask
import pygame as pg
import numpy as np


#-[ NOTE ]-------------------------------------------------------------------------------
# This is a bunch of code i made, takken from the last version of the previous iterations
#----------------------------------------------------------------------------------------


# Global Variables used to manage the duplication of RectBox ID's
new_objectid = 0
num_objectid = 0

# This is rect box side
def point_to_rbox(point:list[int], position:list[int], objectid:int, rbox_key:int=0) -> RectBox:
    global new_objectid, num_objectid

    if new_objectid == objectid: num_objectid += 1
    else: new_objectid = objectid; num_objectid = 0

    """
    **Make RectBox using a point**
    >>> rect_to_dmask([offsetx, offsety], [parentx, parenty], objectid, rbox_key)
    >>> rect_to_dmask(point, position, objectid, rbox_key)
    """
    return RectBox([point[0], point[1], 1, 1], position, int(((new_objectid*10)+num_objectid)), rbox_key)

def rect_to_rbox(offsetrect:list[int], position:list[int], objectid:int, rbox_key:int=0) -> RectBox:
    global new_objectid, num_objectid
    if new_objectid == objectid: num_objectid += 1
    else: new_objectid = objectid; num_objectid = 0
    
    return RectBox([
					int(position[0]), #0
					int(position[1]), #1

					offsetrect[0], #2
					offsetrect[1], #3
					offsetrect[2], #4
					offsetrect[3],  #5

					int(((new_objectid*10)+num_objectid)), #6

					rbox_key

				])


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
