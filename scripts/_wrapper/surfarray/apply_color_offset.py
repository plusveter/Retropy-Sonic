from ..utils import *
import ctypes
import numpy as np
from typing import Any


# ---------------- Declaring the ctypes function signature ----------------

lib.apply_color_offset.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),  # surf input/output
    ctypes.c_int,                    # surf_x
    ctypes.c_int,                    # surf_y
    ctypes.POINTER(ctypes.c_uint8),  # mask
    ctypes.c_int,                    # mask_x
    ctypes.c_int,                    # mask_y
    ctypes.c_int,                    # surf width
    ctypes.c_int,                    # surf height
    ctypes.c_int,                    # mask width
    ctypes.c_int,                    # mask height
]

lib.apply_color_offset.restype = None


# ---------------- Python wrapper function ----------------

def apply_color_offset_wrapper(
    surf_2darray: np.ndarray[Any, Any],
    position_surf:list,
    mask_2darray: np.ndarray[Any, Any],
    position_mask:list,
):
    """Apply a color offset to pixels selected by the mask."""

    # Ensure uint8
    if surf_2darray.dtype != np.uint8:
        surf_2darray = surf_2darray.astype(np.uint8, copy=False)

    if mask_2darray.dtype != np.uint8:
        mask_2darray = mask_2darray.astype(np.uint8, copy=False)

    # Ensure contiguous arrays
    surf_array = np.ascontiguousarray(surf_2darray, dtype=np.uint8)
    mask_array = np.ascontiguousarray(mask_2darray, dtype=np.uint8)

    surf_width, surf_height = surf_array.shape
    mask_width, mask_height = mask_array.shape

    # Call C++
    lib.apply_color_offset(
        surf_array.ctypes.data_as(
            ctypes.POINTER(ctypes.c_uint8)
        ),

        ctypes.c_int(int(position_surf[0])),
        ctypes.c_int(int(position_surf[1])),

        mask_array.ctypes.data_as(
            ctypes.POINTER(ctypes.c_uint8)
        ),

        ctypes.c_int(int(position_mask[0])),
        ctypes.c_int(int(position_mask[1])),

        ctypes.c_int(surf_width),
        ctypes.c_int(surf_height),

        ctypes.c_int(mask_width),
        ctypes.c_int(mask_height),
    )

    return surf_array