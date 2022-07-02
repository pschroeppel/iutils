#!/usr/bin/env python3

import numpy as np
import math
from ._pair_metric import _PairMetric
from .result import Result
from .registry import register_pair_metric
from itypes import is_numpy, is_torch, convert, uint8, FormattedFloat


class PSNRYMetric(_PairMetric):
    _name = "PSNRY"
    _has_error_map = False
    _precision = 2

    def compute(self, data, ref, dims="hwc", device=None, compute_map=False, crop_boundary=4):
        if compute_map:
            raise Exception(f"PSNRY cannot provide error map")

        data_bhwc = convert(data, old_dims=dims, new_dims="bhwc", device="numpy", dtype=uint8)
        ref_bhwc = convert(ref, old_dims=dims, new_dims="bhwc", device="numpy", dtype=uint8)

        if crop_boundary is not None and crop_boundary > 0:
            c = crop_boundary
            ref_bhwc = ref_bhwc[:, c:-c, c:-c, :]
            data_bhwc = data_bhwc[:, c:-c, c:-c, :]

        import cv2

        errors = []
        for i in range(0, data_bhwc.shape[0]):
            data_hwc = data_bhwc[i, ...]
            ref_hwc = ref_bhwc[i, ...]

            data_Y = cv2.cvtColor(data_hwc, cv2.COLOR_RGB2YCrCb)[:, :, 0]
            ref_Y = cv2.cvtColor(ref_hwc, cv2.COLOR_RGB2YCrCb)[:, :, 0]

            mse = np.mean((data_Y - ref_Y)**2)
            if mse == 0: error = float('inf')
            else:        error = 20 * math.log10(255.0 / math.sqrt(mse))

            errors.append(error)

        return Result(
            error=FormattedFloat(sum(errors) / len(errors), self._precision)
        )

register_pair_metric(PSNRYMetric)