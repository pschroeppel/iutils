#!/usr/bin/env python3

from itypes import convert


class Result:
    def __init__(self, error, error_map=None):
        self._error_map = error_map
        self._error = error

    def error(self):
        return self._error

    def map(self, device="numpy", dims="bhwc"):
        return convert(self._error_map, old_dims="bhwc", new_dims=dims, device=device)

