# Testing folds

Testing folds for the LOB dataset. Each file is a compressed text block:

- `Test_Dst_NoAuction_ZScore_CF_1.txt.xz` through
  `Test_Dst_NoAuction_ZScore_CF_9.txt.xz`

## Format

Each file is whitespace-separated text representing a `(rows, timesteps)` matrix.
See `data/README.md` for the full format and how features/labels are extracted.

## Usage in the notebook

- The notebook loads these files with `np.loadtxt`.
- For fold `k`, testing uses the next fold(s) after training (default: fold `k+1`).
- The number of future folds used for testing is controlled by
  `test_horizon_folds` in the loader.

## Decompression

From the project root:

```bash
bash scripts/unxz_data.sh
```

This keeps the `.xz` files and writes `.txt` files alongside them.
