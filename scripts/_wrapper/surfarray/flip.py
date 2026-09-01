from ..utils import *
import ctypes
import numpy as np
from typing import Any


# ---------------- Declaring the ctypes function signature ----------------

lib.flip.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),  # array
    ctypes.c_int,                    # width
    ctypes.c_int,                    # height
    ctypes.c_bool,                   # flip_x
    ctypes.c_bool,                   # flip_y
]

lib.flip.restype = None


# ---------------- Python wrapper function ----------------

def flip_wrapper(
    array: np.ndarray[Any, Any],
    flip_x: bool = False,
    flip_y: bool = False,
) -> np.ndarray[Any, Any]:
    """
    Flip a 2D uint8 NumPy array in-place.

    flip_x=True  -> horizontal flip
    flip_y=True  -> vertical flip
    both=True    -> flip both axes
    """

    if array.dtype != np.uint8:
        raise TypeError("array must have dtype=np.uint8")

    if array.ndim != 2:
        raise ValueError("array must be a 2D array")

    if not array.flags["C_CONTIGUOUS"]:
        raise ValueError(
            "array must be C-contiguous"
        )

    height, width = array.shape

    lib.flip(
        array.ctypes.data_as(
            ctypes.POINTER(ctypes.c_uint8)
        ),
        ctypes.c_int(width),
        ctypes.c_int(height),
        ctypes.c_bool(flip_x),
        ctypes.c_bool(flip_y),
    )

    return array