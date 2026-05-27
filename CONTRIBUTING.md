# Contributing

Contributions should preserve the clean-room nature of the project. Do not paste proprietary or license-incompatible code from regulatory model distributions.

Before opening a pull request, run:

```bash
python -m compileall src tests
python -m pytest
ruff check src tests
mypy src
```

Scientific changes should include a reproducible benchmark, source data provenance, and a comparison against a trusted reference run where licensing allows it.
