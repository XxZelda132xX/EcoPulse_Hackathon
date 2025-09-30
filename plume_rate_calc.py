import sys
import pandas as pd
import numpy as np
import rasterio
import math
from rasterio.transform import xy

def get_wind_for_plume(csv_path: str):
    df = pd.read_csv(csv_path)
    row = df.iloc[0]  # first row

    speed_mps = float(row["wind_speed_avg_auto"])       # m/s
    from_deg  = float(row["wind_direction_avg_auto"])   # meteorological "from" degrees
    emission = float(row["emission_auto"])
    error = float(row["emission_uncertainty_auto"])
    
    return [speed_mps, from_deg, emission, error]

def plume_length_m(mask_tif: str, wind_from_deg: float):
    """
    Measure plume length L (meters) along wind 'to' direction.
    Inputs:
      - mask_tif: path to plume mask GeoTIFF (nonzero pixels = plume)
      - wind_from_deg: meteorological 'from' direction (deg, 0°=N, clockwise)
    Returns:
      (L_m, axis_az_deg) where:
        L_m          = plume length in meters
        axis_az_deg  = azimuth of measurement axis (0°=N, clockwise)
    """
    # met 'from' -> 'to' azimuth (plume travel direction)
    axis_az_deg = (float(wind_from_deg) + 180.0) % 360.0
    # azimuth (0=N, clockwise) -> unit vector (x east, y north)
    theta = math.radians((90.0 - axis_az_deg) % 360.0)
    u = np.array([math.cos(theta), math.sin(theta)], dtype=float)

    # read plume mask and collect plume pixels
    with rasterio.open(mask_tif) as src:
        arr = src.read(1)
        T   = src.transform
        crs = src.crs

    # quick sanity: length is meaningful in projected (meter) CRS
    if crs and crs.to_string().upper().startswith("EPSG:4326"):
        raise ValueError("GeoTIFF CRS is geographic (lat/lon). Reproject to a metric CRS (e.g., UTM) first.")

    rows, cols = np.where(arr > 0)
    if rows.size < 2:
        raise ValueError("Not enough plume pixels (>0).")

    # pixel centers -> map coords (meters in UTM/other projected CRS)
    xs, ys = xy(T, rows, cols)
    X = np.column_stack([np.asarray(xs, float), np.asarray(ys, float)])  # (N,2)

    # project points onto axis and take span
    t = X @ u
    L_m = float(t.max() - t.min())
    return L_m, axis_az_deg

def get_flow_rate(plume_length_m: float, wind_speed_mps: float, ime_kg: float) -> float:
    """
    Q [kg/h] ≈ IME [kg] * (U_parallel / L) * 3600
    Here we assume you measured L along the wind 'to' axis, so U_parallel ≈ wind_speed_mps.
    """
    if plume_length_m <= 0 or wind_speed_mps <= 0 or ime_kg <= 0:
        return float("nan")
    tau_s = plume_length_m / wind_speed_mps
    return (ime_kg / tau_s) * 3600.0  # kg/h

def main(tif_path, csv_path):
    # pull wind + IME (your get_wind_for_plume already returns [U, from_deg, IME, IME_sigma])
    U_mps, wind_from_deg, IME_kg, IME_sigma_kg = get_wind_for_plume(csv_path)

    # measure L along wind-to axis (so U_parallel ≈ U_mps)
    L_m, axis_az = plume_length_m(tif_path, wind_from_deg)

    # ---- rate from IME ----
    rate_kg_per_h = get_flow_rate(L_m, U_mps, IME_kg)
    rate_t_per_h  = rate_kg_per_h / 1000.0

    # optional: IME-only uncertainty propagation
    rate_sigma_tph = (IME_sigma_kg / IME_kg) * rate_t_per_h if IME_kg > 0 else float("nan")

    print(f"L = {L_m:.0f} m, axis ≈ {axis_az:.1f}°, U = {U_mps:.2f} m/s")
    print(f"IME = {IME_kg:,.0f} kg  →  Rate ≈ {rate_t_per_h:.2f} t/h  (± {rate_sigma_tph:.2f} t/h, IME-only)")

if __name__ == "__main__":
    main("tiff_files/plume_3_concentrations.tif", "datasets/plume_3.csv")
