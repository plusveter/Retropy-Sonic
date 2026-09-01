from ..utils import *
import ctypes
import numpy as np
from typing import Any

lib.scale.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),  # src
    ctypes.POINTER(ctypes.c_uint8),  # dst
    ctypes.c_int,                    # width
    ctypes.c_int,                    # height
    ctypes.c_int,                    # new_width
    ctypes.c_int,                    # new_height
]

lib.scale.restype = None


def scale_wrapper(
    array: np.ndarray[Any, Any],
    new_width: int,
    new_height: int,
) -> np.ndarray[Any, Any]:

    if array.dtype != np.uint8:
        raise TypeError("array must have dtype=np.uint8")

    if array.ndim != 2:
        raise ValueError("array must be a 2D array")

    if not array.flags["C_CONTIGUOUS"]:
        raise ValueError("array must be C-contiguous")

    if new_width <= 0: return np.zeros((1, 1), dtype=np.uint8)

    if new_height <= 0: return np.zeros((1, 1), dtype=np.uint8)

    # Array convention: (width, height)
    width, height = array.shape
    new_width, new_height = int(new_width), int(new_height)

    output = np.empty(
        (new_width, new_height),
        dtype=np.uint8,
    )

    lib.scale(
        array.ctypes.data_as(
            ctypes.POINTER(ctypes.c_uint8)
        ),
        output.ctypes.data_as(
            ctypes.POINTER(ctypes.c_uint8)
        ),
        ctypes.c_int(width),
        ctypes.c_int(height),
        ctypes.c_int(new_width),
        ctypes.c_int(new_height),
    )

    return output