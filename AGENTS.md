## Build & Run

```bash
python src/main.py                          # uses default src/data/sample.csv
python src/main.py path/to/data.csv         # custom input
python src/main.py data.csv -o result.json  # custom output path
```

## Validation

```bash
python -m unittest discover -s src/tests -v  # run all tests (31 tests)
```

## Operational Notes

- No external dependencies — Python 3 standard library only
- Output written to `output.json` in current working directory by default
- Exit code 1 on errors (missing file, bad CSV format)
