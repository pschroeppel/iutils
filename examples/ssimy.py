#!/usr/bin/env python3

from itypes import data_root, Dataset, float32
from imetrics import compute_pair_metric

device = "numpy"

reference = data_root.file('scene1/0000-image0.png').read(dims="hwc", device=device, dtype=float32)
data = reference + 0.05

result = compute_pair_metric("SSIMY", data, reference, dims="hwc")

error = result.error()
error_map = result.map(device=device, dims="hwc")

print()
print("SSIMY Error: ", error)

# Create dataset with a single item
ds = Dataset(file='out_ssimy/data.json', single_item=True, auto_write=True)

# Show results
with ds.viz.new_row() as row:
    row.add_cell('image', var='data').sv.set_data(data)
    row.add_cell('image', var='reference').sv.set_data(reference)
    row.add_cell('float', var='result').sv.set_data(error_map)

print()
print("To view run: \"iviz out_ssimy/data.json\"")
print()


