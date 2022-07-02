#!/usr/bin/env python3

_metrics = {}
_instances = {}

def register_pair_metric(_class):
    type = _class._name
    _metrics[type] = _class

def compute_pair_metric(type, *args, **kwargs):
    if type not in _metrics:
        raise Exception(f"unkonwn metric type {type}")

    if type not in _instances:
        _instances[type] = _metrics[type]()

    return _instances[type].compute(*args, **kwargs)

def metric_precision(type):
    if type not in _metrics:
        raise Exception(f"unkonwn metric type {type}")

    return _metrics[type]._precision


def available_pair_metrics():
    return _metrics.keys()