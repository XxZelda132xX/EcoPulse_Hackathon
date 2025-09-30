# pip install rasterio
import sys
import numpy as np
import rasterio
from rasterio.transform import xy

def main(path):
    with rasterio.open(path) as src:
        arr = src.read(1)            # first band
        T   = src.transform          # affine transform
        crs = src.crs                # coordinate system

    # Find the first nonzero pixel (fallback to image center)
    nz = np.argwhere(arr > 0)
    if nz.size == 0:
        r = arr.shape[0] // 2
        c = arr.shape[1] // 2
        reason = "no nonzero pixels found; using image center"
    else:
        r, c = nz[0]
        reason = "first nonzero pixel"

    x, y = xy(T, r, c)

    print(f"File: {path}")
    print(f"CRS: {crs}")
    print(f"Transform: {T}")
    print(f"Picked pixel: row={r}, col={c} ({reason})")
    print(f"Map coords: x={x:.3f}, y={y:.3f}")
    print("Note: if CRS is geographic (EPSG:4326), x/y are degrees; if projected (e.g., UTM), x/y are meters.")

if __name__ == "__main__":
    main("tiff_files/plume_3.tif")
