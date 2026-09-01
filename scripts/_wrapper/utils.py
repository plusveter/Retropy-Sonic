from retropy import * 
from typing import List, TypedDict, TypeVar, Any, Dict, NamedTuple
import ctypes
import numpy as np

# Load the shared library
lib = ctypes.CDLL('./packages.mdll')
