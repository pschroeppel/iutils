#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iUtils                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/iutils  ###
### --------------------------------------- ###

import time
import threading
import sys
import logging
from itypes import psep

log = logging.getLogger('profiler')


def _formatted_time(time):
    if time < 1000:
        return '%.1fms' % (time)
    else:
        sec = time / 1000
        if sec < 60:
            return '%.3fs' % (sec)
        else:
            min = int(sec / 60)
            sec = sec - min * 60
            return '%dm%.3fs' % (min, sec)


class _ProfileTime:
    def __init__(self, name, total_start_time):
        self._name = name
        self._start_time = None
        self._total_start_time = total_start_time
        self._durations = []
        self._total_time = 0
        self._num_iters = 0

    def name(self):
        return self._name

    def start(self):
        self._start_time = time.time()

    def stop(self):
        if self._start_time is None:
            return

        duration = time.time() - self._start_time
        self._num_iters += 1
        self._total_time += duration
        self._durations.append(duration)
        self._start_time = None

        while len(self._durations) > 100:
            self._durations.pop(0)

    def total_num_execs(self):
        return self._num_iters

    def formatted_total_num_execs(self):
        return '%d' % self.total_num_execs()

    def total(self):
        return self._total_time * 1000 # ms

    def total_fraction(self):
        return self._total_time / (time.time() - self._total_start_time)

    def formatted_total_fraction(self):
        return '%3.2f%%' % (self.total_fraction() * 100)

    def formatted_total(self):
        return _formatted_time(self.total())

    def total_average(self):
        if self._num_iters == 0:
            return None
        return self._total_time / self._num_iters * 1000 # ms

    def formatted_total_average(self):
        total_average = self.total_average()
        if total_average is None:
            return None
        return _formatted_time(total_average)

    def running_average(self):
        if len(self._durations) == 0:
            return None
        return sum(self._durations) / len(self._durations) * 1000 # ms

    def formatted_running_average(self):
        running_average = self.running_average()
        if running_average is None: return None
        return _formatted_time(running_average)


class _Scope:
    def __init__(self, name):
        self._name = name

    def __enter__(self):
        profiler.start(self._name)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        profiler.stop(self._name)
        if exc_type is None:
            return self
            
            
class Profiler:
    def __init__(self, synchronized = False):
        self._items = {}
        self._total_items = {}
        self._timer = None
        self._profile_every = None
        self._synchronized = synchronized
        self._start_time = time.time()

    def __getitem__(self, item):
        if item not in self._items:
            self._items[item] = _ProfileTime(item, self._start_time)

        return self._items[item]

    def scope(self, name):
        return _Scope(name)

    def set_synchronized(self, value):
        if value:
            log.warning("Running in CUDA synchronized mode")
        self._synchronized = value

    def print_summary(self, final=False):
        psep('Profiler Info:', sep_char='*', width=120)

        max_name_len = 0
        for item in self._items.values():
            max_name_len = max(max_name_len, len(item.name()))

        items = list(self._items.values())

        colums = {}
        colums["Name"] = max_name_len
        colums["R. Avg."] = 10
        colums["T. Avg."] = 10
        colums["# Execs"] = 10
        colums["Total"] = 10
        colums["% Total"] = 10

        def print_columns(*cols):
            i = 0
            for width in colums.values():
                data = str(cols[i])
                align = ''
                if i == 0: align = '-'
                print(('%' + align + str(width) + 's |') % data, end='')
                i += 1
            print()

        def print_hline():
            for width in colums.values():
                data = '-' * (width + 2)
                print(data, end='')
            print()

        print_columns(*colums.keys())
        print_hline()

        for item in items:
            print_columns(
                item.name(),
                item.formatted_running_average(),
                item.formatted_total_average(),
                item.formatted_total_num_execs(),
                item.formatted_total(),
                item.formatted_total_fraction()
            )

        psep(sep_char='*', width=120)
        sys.stdout.flush()

        print('Total time:', _formatted_time(self.total_time()))

    def total_time(self):
        return (time.time() - self._start_time) * 1000 # ms

    def print_final_summary(self):
        self.print_summary(final=True)
        self.shutdown()

    def _start_timer(self):
        self._timer = threading.Timer(self._profile_every, self._timer_elapsed)
        self._timer.start()

    def _stop_timer(self):
        if self._timer is None:
            return

        self._timer.cancel()
        self._timer = None

    def profile_every(self, seconds):
        self._profile_every = seconds
        if seconds is None:
            self._stop_timer()
        else:
            self._start_timer()

    def shutdown(self):
        self._profile_every = None
        self._stop_timer()

    def _timer_elapsed(self):
        self._timer = None
        self.print_summary()
        if self._profile_every:
            self._start_timer()

    def start(self, name):
        self[name].start()

    def stop(self, name):
        if self._synchronized:
            import torch
            torch.cuda.synchronize()
        self[name].stop()

profiler = Profiler()
