# PyWRF and PyMET interoperability

PyPuff uses clean-room module names for the WRF-to-meteorology part of the workflow:

- **PyWRF** (`pypuff.models.pywrf`) is the former CALWRF role.  It reads WRF/WRF-like NetCDF data, extracts near-surface wind, and can download WRF5 d03 history files from the meteo@uniparthenope archive.
- **PyMET** (`pypuff.models.pymet`) is the former CALMET role for local diagnostic interpolation use cases.  It creates a local projected grid and writes NetCDF-CF meteorological fields consumed by PyPuff dispersion modules.

These modules are not translations of the original Fortran code.  They are Python APIs that implement a compatible workflow and prefer NetCDF-CF interchange.

## meteo@uniparthenope WRF5 d03 archive

The downloader constructs URLs using this pattern:

```text
https://data.meteo.uniparthenope.it/files/wrf5/d03/history/YYYY/MM/DD/wrf5_d03_YYYYMMDDZhh00.nc
```

Example URL construction from Python:

```python
from pypuff.models.pywrf import meteo_uniparthenope_wrf_url

url = meteo_uniparthenope_wrf_url("2026-05-27", 0)
print(url)
```

Download from Python:

```python
from pypuff.models.pywrf import download_meteo_uniparthenope_wrf

path = download_meteo_uniparthenope_wrf("data/wrf", run_date="2026-05-27", cycle_hour=0)
```

Use case 01 exposes the same downloader from the command line.

## PyWRF to PyMET pipeline

```python
from pypuff.models import pywrf, pymet

wrf = pywrf.load_near_surface_wind("data/wrf/wrf5_d03_20260527Z0000.nc")
met = pymet.downscale_wrf_to_local_grid(
    wrf,
    center_lat=40.85,
    center_lon=14.27,
    nx=101,
    ny=101,
    dx_m=100,
    dy_m=100,
)
pymet.write_local_meteorology("output/wrf_100m_wind.nc", met)
```

## Output conventions

PyMET writes a NetCDF-CF product containing local x/y, latitude/longitude, eastward/northward wind, wind speed, and meteorological wind direction.  JSON fallback is available for test and low-dependency environments.
