# Examples

`minimal.json` and `minimal.inp` describe the same synthetic domain: a 5 x 4 local grid, two stations, one point source, and two receptors.

Recommended interoperability workflow uses NetCDF-CF:

```bash
pypuff run examples/minimal.json --output-dir output --interchange netcdf
pypuff run examples/minimal.inp --output-dir output-particles --backend particles --interchange netcdf
pypuff-plot --input output/concentration.nc --output output/concentration.png
```

Legacy-compatible text/CSV workflow is still available:

```bash
pycalmet --config examples/minimal.inp --output output/meteo.json --format json
pypuff-model --config examples/minimal.inp --meteo output/meteo.json --output output/concentration.csv --format csv
pypuff-particles --config examples/minimal.inp --meteo output/meteo.json --output output/particle_concentration.csv --format csv
pycalpost --input output/concentration.csv --output output/post.json
```
