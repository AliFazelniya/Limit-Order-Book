# Limit Order Book (LOB) Sequence Classification

Experiments and data preparation for LOB sequence classification using pre-split
walk-forward folds and a reference training notebook. Data are stored as
LZMA-compressed whitespace matrices (`.txt.xz`) and loaded into NumPy for
sliding-window construction.

## Layout

- `data/` - compressed training/testing folds (see `data/README.md`).
- `notebooks/` - training and evaluation notebook (see `notebooks/README.md`).
- `scripts/` - dataset utilities (see `scripts/README.md`).
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

## Data model (as used by the notebook)

- Each fold is a 2D array `data` with shape `(R, T)` loaded via `np.loadtxt`.
- Columns are timesteps; rows are variables.
- Features: `X = data[:num_features, :].T` (default `num_features=144`).
- Labels: `y = data[-horizon, :][seq_size - 1:] - 1`.
- Sliding window sample `i` spans timesteps `[i, i+seq_size-1]` and uses `y[i]`.
- Horizon mapping: `1 -> 100`, `2 -> 50`, `3 -> 30`, `4 -> 20`, `5 -> 10` ticks.

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
