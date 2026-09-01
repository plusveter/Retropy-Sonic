from ..utils import *

# ---------------- Declaring the ctypes function signature ----------------
lib.perfect_vertical_scroll.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),   # input
    ctypes.POINTER(ctypes.c_double),  # array1D
    ctypes.c_int,                     # array_len (must == width)
    ctypes.c_int,                     # roll
    ctypes.c_int,                     # width
    ctypes.c_int,                     # height
    ctypes.POINTER(ctypes.c_uint8)    # output
]
lib.perfect_vertical_scroll.restype = ctypes.c_int

# ---------------- Python wrapper function ----------------
def perfect_vertical_scroll_wrapper(surf_array: np.ndarray[Any, Any], array_1D, roll):
    """ Perform a perfect vertical roll on the given 1D array. """
    h, w = surf_array.shape
    arr = np.ascontiguousarray(surf_array, dtype=np.uint8)
    offs = np.ascontiguousarray(array_1D, dtype=np.float64)
    if offs.size != w:
        raise ValueError(f"array_1D length {offs.size} must equal width {w} for vertical scroll")

    out = np.empty_like(arr)
    status = lib.perfect_vertical_scroll(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
        offs.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        ctypes.c_int(offs.size),
        ctypes.c_int(roll),
        ctypes.c_int(w),
        ctypes.c_int(h),
        out.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
    )
    if status != 0:
        raise RuntimeError(f"perfect_vertical_scroll failed with code {status}")
    return out