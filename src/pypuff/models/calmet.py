from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import numpy as np

from pypuff.config import SuiteConfig
from pypuff.core.grid import Grid
from pypuff.core.physics import wind_components
from pypuff.io.jsonio import write_json
from pypuff.io.legacy_outputs import infer_format
from pypuff.io.netcdf_cf import write_cf_meteorology


def build_meteorology(config: SuiteConfig, power: float = 2.0) -> dict[str, object]:
    """Build a deterministic CALMET-like diagnostic field.

    Station wind vector, temperature, and mixing height are interpolated by
    inverse-distance weighting. The preferred interchange format is NetCDF-CF,
    while JSON and legacy text remain available for compatibility workflows.
    """
    config.validate()
    if power <= 0:
        raise ValueError("interpolation power must be positive")
    grid = Grid(**asdict(config.grid))
    xx, yy = grid.mesh()
    u = np.zeros((grid.ny, grid.nx), dtype=float)
    v = np.zeros_like(u)
    temp = np.zeros_like(u)
    mixh = np.zeros_like(u)
    weights = np.zeros_like(u)

    if not config.stations:
        u.fill(float(config.run.get("default_u", 2.0)))
        v.fill(float(config.run.get("default_v", 0.0)))
        temp.fill(float(config.run.get("default_temperature", 293.15)))
        mixh.fill(float(config.run.get("default_mixing_height", 1000.0)))
    else:
        for station in config.stations:
            dist = np.hypot(xx - station.x, yy - station.y)
            w = 1.0 / np.maximum(dist, 1.0) ** power
            su, sv = wind_components(station.wind_speed, station.wind_dir)
            u += w * su
            v += w * sv
            temp += w * station.temperature
            mixh += w * station.mixing_height
            weights += w
        u = np.divide(u, weights, out=np.zeros_like(u), where=weights > 0)
        v = np.divide(v, weights, out=np.zeros_like(v), where=weights > 0)
        temp = np.divide(temp, weights, out=np.full_like(temp, 293.15), where=weights > 0)
        mixh = np.divide(mixh, weights, out=np.full_like(mixh, 1000.0), where=weights > 0)

    speed = np.hypot(u, v)
    return {
        "component": "calmet",
        "grid": asdict(config.grid),
        "u": u.tolist(),
        "v": v.tolist(),
        "wind_speed": speed.tolist(),
        "temperature": temp.tolist(),
        "mixing_height": mixh.tolist(),
        "stations": [asdict(s) for s in config.stations],
        "metadata": {"kernel": "inverse-distance diagnostic", "schema_version": "1.1"},
    }


def run(config: SuiteConfig, output: str | Path, output_format: str = "auto") -> dict[str, object]:
    result = build_meteorology(config)
    fmt = infer_format(output, output_format)
    if fmt == "netcdf":
        write_cf_meteorology(output, result)
    else:
        write_json(output, result)
    return result
