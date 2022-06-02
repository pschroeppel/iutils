#!/usr/bin/env python3

from numpy.ctypeslib import ndpointer
import ctypes
import numpy as np
import os


lib = ctypes.cdll.LoadLibrary('libivizutils.so')


#
# flow_viz_sintel
#
c_flow_viz_sintel = lib.flow_viz_sintel
c_flow_viz_sintel.restype = None
c_flow_viz_sintel.argtypes = [ndpointer(ctypes.c_float, flags='C_CONTIGUOUS'),
                       ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'),
                       ctypes.c_int,
                       ctypes.c_int,
                       ctypes.c_float]

def flow_viz_sintel(flow, scale):
    cont_flow = np.ascontiguousarray(flow, np.float32)
    height, width = flow.shape[0], flow.shape[1]

    result = np.zeros((height, width, 3), dtype=np.uint8)

    c_flow_viz_sintel(cont_flow, result, width, height, scale)

    return result


#
# flow_viz_middlebury
#
c_flow_viz_middlebury = lib.flow_viz_middlebury
c_flow_viz_middlebury.restype = None
c_flow_viz_middlebury.argtypes = [ndpointer(ctypes.c_float, flags='C_CONTIGUOUS'),
                       ndpointer(ctypes.c_ubyte, flags='C_CONTIGUOUS'),
                       ctypes.c_int,
                       ctypes.c_int,
                       ctypes.c_float]

def flow_viz_middlebury(flow, scale):
    cont_flow = np.ascontiguousarray(flow, np.float32)
    height, width = flow.shape[0], flow.shape[1]

    result = np.zeros((height, width, 3), dtype=np.uint8)

    c_flow_viz_middlebury(cont_flow, result, width, height, scale)

    return result


#
# flow_viz
#
def flow_viz(flow, scale, type="sintel"):
    if type not in ["sintel", "middlebury"]:
        raise Exception(f"\"{type}\" invalid for flow_viz type=... must be \"sintel\" or \"middlebury\"")

    if type == "middlebury":
        return flow_viz_middlebury(flow, scale)
    else:
        return flow_viz_sintel(flow, scale)
