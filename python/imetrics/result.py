#!/usr/bin/env python3

from itypes import convert


class Result:
    def __init__(self, error, error_map=None, precision=2):
        self._error_map = error_map
        self._error = error
        self._precision = precision

    def error(self):
        return self._error

    def formatted(self):
        return f"{self._error:.{self._precision}f}"

    def map(self, device, dims="bhwc"):
        return convert(self._error_map, old_dims="bhwc", new_dims=dims, device=device)

