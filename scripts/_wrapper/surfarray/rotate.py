from ..utils import *
import math

# ---------------- Declaring the ctypes function signature ----------------
lib.rotate.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),  # src
    ctypes.POINTER(ctypes.c_uint8),  # dst
    ctypes.c_int,                     # width
    ctypes.c_int,                     # height
    ctypes.c_int,                     # channels
    ctypes.c_double                   # angle
]
lib.rotate.restype = None

# ---------------- Python wrapper function ----------------
def rotate_wrapper(surf_array: np.ndarray[Any, Any], angle: float) -> np.ndarray:
    """
    Rotate a 2D grayscale numpy array by `angle` degrees.
    Returns a new rotated array with expanded dimensions.
    """
    h, w = surf_array.shape[:2]
    channels = surf_array.shape[2] if surf_array.ndim == 3 else 1

    # Compute expanded dimensions
    rad = np.deg2rad(angle)
    new_w = int(abs(w*np.cos(rad)) + abs(h*np.sin(rad)))
    new_h = int(abs(w*np.sin(rad)) + abs(h*np.cos(rad)))

    dst = np.zeros((new_h, new_w, channels), dtype=np.uint8)

    lib.rotate(
        surf_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
        dst.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
        w, h, channels, float(angle)
    )

    # Convert to 2D by averaging channels if needed
    if dst.ndim == 3 and dst.shape[2] > 1:
        dst_2d = dst.mean(axis=2).astype(np.uint8)
    else:
        dst_2d = dst[:, :, 0] if dst.ndim == 3 else dst

    return dst_2d