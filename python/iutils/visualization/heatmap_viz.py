#!/usr/bin/env python3

from numpy.ctypeslib import ndpointer
import ctypes
import numpy as np
import os


lib = ctypes.cdll.LoadLibrary('libivizutils.so')


#
# heat_map_viz
#
c_heat_map_viz = lib.heatmap_viz
c_heat_map_viz.restype = None
c_heat_map_viz.argtypes = [ndpointer(ctypes.c_float, flags='C_CONTIGUOUS'),
                       ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'),
                       ctypes.c_int,
                       ctypes.c_int,
                       ctypes.c_float,
                       ctypes.c_float]

def heatmap_viz(data, min, max):
    cont_data = np.ascontiguousarray(data, np.float32)
    height, width = data.shape[0], data.shape[1]

    result = np.zeros((height, width, 3), dtype=np.uint8)

    c_heat_map_viz(cont_data, result, width, height, min, max)

    return result


