#!/usr/bin/env python3

import numpy as np
import math
from ._pair_metric import _PairMetric
from .result import Result
from .registry import register_pair_metric
from itypes import is_numpy, is_torch, convert, uint8, FormattedFloat


class SSIMYMetric(_PairMetric):
    _name = "SSIMY"
    _has_error_map = False
    _precision = 3

    def compute(self, data, ref, dims="hwc", device=None, compute_map=False, crop_boundary=4):
        data_bhwc = convert(data, old_dims=dims, new_dims="bhwc", device="numpy", dtype=uint8)
        ref_bhwc = convert(ref, old_dims=dims, new_dims="bhwc", device="numpy", dtype=uint8)
        s = data_bhwc.shape

        if crop_boundary is not None and crop_boundary > 0:
            c = crop_boundary
            ref_bhwc = ref_bhwc[:, c:-c, c:-c, :]
            data_bhwc = data_bhwc[:, c:-c, c:-c, :]

        import cv2
        C1 = (0.01 * 255) ** 2
        C2 = (0.03 * 255) ** 2

        error_map = np.zeros((s[0], s[1], s[2], 1))
        errors = []
        for i in range(0, data_bhwc.shape[0]):
            data_hwc = data_bhwc[i, ...]
            ref_hwc = ref_bhwc[i, ...]

            data_Y = cv2.cvtColor(data_hwc, cv2.COLOR_RGB2YCrCb)[:, :, 0]
            ref_Y = cv2.cvtColor(ref_hwc, cv2.COLOR_RGB2YCrCb)[:, :, 0]

            img1 = data_Y
            img2 = ref_Y

            kernel = cv2.getGaussianKernel(11, 1.5)
            window = np.outer(kernel, kernel.transpose())

            mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
            mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
            mu1_sq = mu1 ** 2
            mu2_sq = mu2 ** 2
            mu1_mu2 = mu1 * mu2
            sigma1_sq = cv2.filter2D(img1 ** 2, -1, window)[5:-5, 5:-5] - mu1_sq
            sigma2_sq = cv2.filter2D(img2 ** 2, -1, window)[5:-5, 5:-5] - mu2_sq
            sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

            # NOTE: ssim_map is 10px smaller than original image
            ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                                                    (sigma1_sq + sigma2_sq + C2))

            pad = (s[1] - ssim_map.shape[0]) // 2
            error_map[i, pad:-pad, pad:-pad, 0] = ssim_map

            errors.append(ssim_map.mean())

        return Result(
            error=FormattedFloat(sum(errors) / len(errors), self._precision)
        )

register_pair_metric(SSIMYMetric)