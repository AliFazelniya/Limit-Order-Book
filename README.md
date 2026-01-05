# Limit Order Book Classification Experiments

Experiments and data prep for limit order book (LOB) classification using the provided
train/test folds and a single training notebook.

## Layout

- `data/` - compressed training/testing folds (see `data/README.md`).
- `notebooks/` - training and evaluation notebook (see `notebooks/README.md`).
- `scripts/` - helpers for decompression and txt-to-csv conversion
  (see `scripts/README.md`).
- `url.txt` - dataset and reference links.

## Quickstart

1. Decompress the dataset files:

   ```bash
   bash scripts/unxz_data.sh
   ```

2. Open the notebook:

   ```bash
   jupyter lab notebooks/train.ipynb
   ```

## Data format (as used by the notebook)

- Raw files are whitespace-separated `.txt` blocks.
- Features are taken from the first `num_features` rows.
- Labels come from the horizon row and are shifted from (1, 2, 3) to (0, 1, 2).
- Horizon mapping: 1 -> 100 ticks, 2 -> 50, 3 -> 30, 4 -> 20, 5 -> 10.

See `data/README.md` for details on file names and folders.

## Dependencies

The notebook uses standard scientific Python libraries. Install what you need for your
environment, for example:

- Python 3.9+
- numpy, pandas, matplotlib, scikit-learn, tqdm
- torch
- jupyter (lab or notebook)
- `unxz` (from xz-utils) for decompression

## References

`url.txt` lists the dataset source and related papers or data format references.
