# Data

This directory contains the train/test folds for the limit order book dataset.
Files are stored as compressed text blocks (`.txt.xz`).

## Layout

- `training/Train_Dst_NoAuction_ZScore_CF_1.txt.xz` through
  `training/Train_Dst_NoAuction_ZScore_CF_9.txt.xz`
- `testing/Test_Dst_NoAuction_ZScore_CF_1.txt.xz` through
  `testing/Test_Dst_NoAuction_ZScore_CF_9.txt.xz`

The notebook expects the corresponding `.txt` files after decompression.

## File format (as used in the notebook)

- Each file is whitespace-separated text and loads into a 2D array
  `(rows, timesteps)` via `np.loadtxt`.
- Columns represent time steps (LOB snapshots).
- Rows represent variables over time:
  - The first `num_features` rows are input features (default: 144).
  - The last rows include labels for different horizons; the notebook picks a
    specific horizon row from the bottom.
- Labels are shifted from `(1, 2, 3)` to `(0, 1, 2)` for modeling.
- Sliding windows are built across timesteps. With `seq_size`, each window is
  length `seq_size` and the label aligns to the last timestep in that window.

Concrete index mapping used by the notebook:

- Let `data` be shape `(R, T)` where `T` is timesteps.
- Features: `X = data[:num_features, :].T` so each sample is a column slice.
- Labels for a given `horizon` are `y = data[-horizon, :][seq_size - 1:] - 1`.
- Window `i` uses timesteps `i..i+seq_size-1` and label `y[i]`.

Horizon mapping used by the notebook:

- `1 -> 100` ticks
- `2 -> 50` ticks
- `3 -> 30` ticks
- `4 -> 20` ticks
- `5 -> 10` ticks

## Fold usage

The notebook uses an expanding window: folds `1..k` for training, then fold `k+1`
for testing (default `test_horizon_folds=1`). When `val_ratio > 0`, the validation
split is time-ordered from the end of the training set to avoid leakage.

## Decompression

From the project root:

```bash
bash scripts/unxz_data.sh
```

Notes:

- Requires `unxz` (from `xz-utils`).
- Keeps the `.xz` files and writes `.txt` files alongside them.
The conversion is streamed line-by-line and writes each `.csv` next to its `.txt`.
