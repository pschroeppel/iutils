#!/usr/bin/env python3

import numpy as np
import math
from ._pair_metric import _PairMetric
from .result import Result
from .registry import register_pair_metric
from itypes import is_numpy, is_torch, convert, uint8


class SSIMYMetric(_PairMetric):
    _name = "SSIMY"
    _has_error_map = False
    _precision = 3

    def compute(self, data, reference, dims="hwc", device=None, compute_map=False):
        if compute_map:
            raise Exception(f"PSNRY cannot provide error map")

        data_bhwc = convert(data, old_dims=dims, new_dims="bhwc", device="numpy", dtype=uint8)
        reference_bhwc = convert(reference, old_dims=dims, new_dims="bhwc", device="numpy", dtype=uint8)

        import cv2
        C1 = (0.01 * 255) ** 2
        C2 = (0.03 * 255) ** 2

        errors = []
        for i in range(0, data_bhwc.shape[0]):
            data_hwc = data_bhwc[i, ...]
            reference_hwc = reference_bhwc[i, ...]

            data_Y = cv2.cvtColor(data_hwc, cv2.COLOR_RGB2YCrCb)[:, :, 0]
            reference_Y = cv2.cvtColor(reference_hwc, cv2.COLOR_RGB2YCrCb)[:, :, 0]

            img1 = data_Y
            img2 = reference_Y

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

            errors.append(ssim_map.mean())

        return Result(
            error=sum(errors) / len(errors),
            precision=self._precision
        )

register_pair_metric(SSIMYMetric)