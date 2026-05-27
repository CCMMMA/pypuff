from __future__ import annotations

from pathlib import Path
from typing import Any

from pypuff.io.jsonio import write_json


def describe_wrf_input(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    result: dict[str, Any] = {"component": "calwrf", "path": str(p), "exists": p.exists()}
    if not p.exists():
        return result
    result["size_bytes"] = p.stat().st_size
    try:
        from netCDF4 import Dataset  # type: ignore
    except Exception:
        result["netcdf"] = "netCDF4 not installed; metadata only"
        return result
    with Dataset(p) as ds:
        result["dimensions"] = {name: len(dim) for name, dim in ds.dimensions.items()}
        result["variables"] = sorted(ds.variables.keys())[:100]
        result["attrs"] = {name: str(getattr(ds, name)) for name in ds.ncattrs()}
    return result


def run(input_path: str | Path, output: str | Path) -> dict[str, Any]:
    result = describe_wrf_input(input_path)
    write_json(output, result)
    return result
