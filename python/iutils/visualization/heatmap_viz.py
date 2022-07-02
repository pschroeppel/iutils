#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iUtils                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/iutils  ###
### --------------------------------------- ###

def heatmap_viz(data, min, max):
    from numpy.ctypeslib import ndpointer
    import ctypes
    import numpy as np

    lib = ctypes.cdll.LoadLibrary('libiutils.so')

    c_heat_map_viz = lib.heatmap_viz
    c_heat_map_viz.restype = None
    c_heat_map_viz.argtypes = [ndpointer(ctypes.c_float, flags='C_CONTIGUOUS'),
                               ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'),
                               ctypes.c_int,
                               ctypes.c_int,
                               ctypes.c_float,
                               ctypes.c_float]

    cont_data = np.ascontiguousarray(data, np.float32)
    height, width = data.shape[0], data.shape[1]

    result = np.zeros((height, width, 3), dtype=np.uint8)

    c_heat_map_viz(cont_data, result, width, height, min, max)

    return result


