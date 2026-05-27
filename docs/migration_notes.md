# Migration notes

The legacy suite archives were used only to identify component names and public file roles. The Python package uses independent source code, synthetic examples, and a clean-room implementation boundary.

PyTerrel and PyMakegeo are style references for packaging, CLI-first operation, JSON configuration, tolerant legacy parsing, tests, and documentation.

Recommended migration path:

1. validate legacy `.inp` files with `pypuff validate`;
2. run CALMET to NetCDF-CF with `pycalmet --format netcdf`;
3. compare Gaussian and particle backends with the same config and `meteo.nc`;
4. postprocess with CALPOST-compatible summaries;
5. publish plots with `pypuff-plot`;
6. add project-specific parser extensions for unsupported legacy keys while preserving unknown values in `run` / `raw`.
