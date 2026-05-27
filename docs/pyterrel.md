# PyTerrel terrain preprocessing

PyTerrel is the clean-room PyPuff component that covers the TERREL role. It does not include, translate, or embed original TERREL or CALPUFF source code. Its purpose is to prepare terrain elevations for the PyPuff modeling grid and for downstream PyMET, MAKEGEO, and dispersion workflows.

## Responsibilities

PyTerrel provides four production tasks:

1. read a terrain raster, currently lightweight ASCII grid input for repository tests and examples;
2. construct the same local azimuthal-equidistant grid convention used by PyMET;
3. interpolate terrain elevations to that local grid with deterministic bilinear interpolation;
4. write a NetCDF-CF terrain product by preference, or JSON when NetCDF support is not installed.

## Command-line use

```bash
pyterrel \
  --terrain examples/terrain.asc \
  --output output/terrain.nc \
  --center-lat 40.85 \
  --center-lon 14.27 \
  --nx 101 --ny 101 \
  --dx 100 --dy 100
```

Use `--json` to force the lightweight JSON fallback:

```bash
pyterrel --terrain examples/terrain.asc --output output/terrain.json \
  --center-lat 40.85 --center-lon 14.27 --json
```

## Python API

```python
from pypuff.models import pyterrel

result = pyterrel.run(
    "examples/terrain.asc",
    "output/terrain.nc",
    center_lat=40.85,
    center_lon=14.27,
    nx=101,
    ny=101,
    dx_m=100.0,
    dy_m=100.0,
)
```

## Interoperability

The NetCDF-CF output contains:

- `x`, `y` local grid coordinates in metres;
- `latitude`, `longitude` geographic coordinates;
- `surface_altitude` terrain elevation in metres.

This makes the product directly usable by PyMET, MAKEGEO-style geophysical tables, visualization, and future terrain-aware dispersion refinements.

## Production notes

The current PyTerrel implementation is intentionally conservative and deterministic. For operational terrain deployments, use a documented DEM source and record its horizontal datum, vertical datum, native resolution, and preprocessing steps. The example ASCII-grid reader is suitable for tutorials and small tests; production deployments should add project-specific DEM adapters under the same clean-room boundary.
