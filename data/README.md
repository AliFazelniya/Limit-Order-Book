# Data

This directory contains the train/test folds for the limit order book dataset.
Files are stored as LZMA-compressed whitespace matrices (`.txt.xz`).

## Layout

- `training/Train_Dst_NoAuction_ZScore_CF_{1..9}.txt.xz`
- `testing/Test_Dst_NoAuction_ZScore_CF_{1..9}.txt.xz`

The notebook expects the corresponding `.txt` files after decompression.

## File format (notebook contract)

Each file is whitespace-separated text and loads into a 2D array `data` with
shape `(R, T)` via `np.loadtxt`.

- `T` = timesteps (LOB snapshots).
- `R` = variables; the first `num_features` rows are inputs (default: 144).
- Label rows are appended at the bottom; the notebook selects by `horizon`.

Feature/label extraction used in the notebook:

- Features: `X = data[:num_features, :].T` (shape `(T, num_features)`).
- Label row: `label_row = data[-horizon, :]`.
- Labels: `y = label_row[seq_size - 1:] - 1`.
- Window `i` uses timesteps `i..i+seq_size-1` and label `y[i]`.

Horizon mapping used by the notebook:

- `1 -> 100` ticks
- `2 -> 50` ticks
- `3 -> 30` ticks
- `4 -> 20` ticks
- `5 -> 10` ticks

## Fold usage

The notebook uses an expanding window: folds `1..k` for training, then fold
`k+1` for testing (default `test_horizon_folds=1`). When `val_ratio > 0`, the
validation split is time-ordered from the end of the training set to avoid
leakage.

## Decompression

From the project root:

```bash
bash scripts/unxz_data.sh
```

Notes:

- Requires `unxz` (from `xz-utils`).
- Keeps the `.xz` files and writes `.txt` files alongside them.
