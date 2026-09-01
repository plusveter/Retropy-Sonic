from ..utils import *

# ---------------- Declaring the ctypes function signature ----------------
lib.fake_alpha.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),  # input
    ctypes.c_uint8,                  # alpha (0–255)
    ctypes.c_uint8,                  # colorkey
    ctypes.c_int,                    # width
    ctypes.c_int,                    # height
    ctypes.POINTER(ctypes.c_uint8)   # output
]
lib.fake_alpha.restype = None

# ---------------- Python wrapper function ----------------
def fake_alpha_wrapper(surf_array: np.ndarray[Any, Any], alpha: int, colorkey: int = 0):
    """Apply fake alpha dithering (0–255) to surf_array."""

    if surf_array.dtype != np.uint8: surf_array = surf_array.astype(np.uint8, copy=False)

    # Ensure contiguous uint8 array
    input_array = np.ascontiguousarray(surf_array, dtype=np.uint8)
    output_array = np.empty_like(input_array)

    height, width = input_array.shape

    # Call the C++ function
    lib.fake_alpha(
        input_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
        ctypes.c_uint8(alpha),
        ctypes.c_uint8(colorkey),
        ctypes.c_int(width),
        ctypes.c_int(height),
        output_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
    )

    return output_array