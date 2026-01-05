# Training folds

Training folds for the LOB dataset. Each file is a compressed text block:

- `Train_Dst_NoAuction_ZScore_CF_1.txt.xz` through
  `Train_Dst_NoAuction_ZScore_CF_9.txt.xz`

## Format

Each file is whitespace-separated text representing a `(rows, timesteps)` matrix.
See `data/README.md` for the full format and how features/labels are extracted.

## Usage in the notebook

- The notebook loads these files with `np.loadtxt`.
- For fold `k`, training uses all files `1..k` (expanding window).
- Validation (if enabled) is a time-ordered split from the end of the training set.

## Decompression

From the project root:

```bash
bash scripts/unxz_data.sh
```

This keeps the `.xz` files and writes `.txt` files alongside them.
