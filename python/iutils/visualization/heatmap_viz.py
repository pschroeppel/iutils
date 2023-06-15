#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iUtils                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/iutils  ###
### --------------------------------------- ###

def heatmap_viz(data, min, max):
    from .vis import vis_2d_array
    result = vis_2d_array(data, out_format={'type': 'np'}, clipping=True, upper_clipping_thresh=max, lower_clipping_thresh=min,).transpose([1, 2, 0])
    return result


