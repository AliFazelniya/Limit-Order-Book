# Scripts

Small helpers for preparing the dataset files.

## unxz_data.sh

Decompress all `.xz` files under `data/` and keep the originals.

```bash
bash scripts/unxz_data.sh
```

Notes:

- Requires `unxz` (from `xz-utils`) on your PATH.
- Writes `.txt` files alongside the `.xz` files it decompresses.
- Safe to re-run; existing `.txt` files are overwritten only if the decompressor
  does so (default behavior).
