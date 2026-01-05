# Scripts

Small helpers for preparing the dataset files.

## unxz_data.sh

Decompress all `.xz` files under `data/` and keep the originals.

```bash
bash scripts/unxz_data.sh
```

Notes:

- Uses `set -euo pipefail` and fails fast on missing dependencies.
- Recursively finds `*.xz` under `data/` and runs `unxz -k` on each file.
- Requires `unxz` (from `xz-utils`) on your PATH.
- Writes `.txt` files alongside the `.xz` files it decompresses.
- Safe to re-run; existing `.txt` files are overwritten only if the decompressor
  does so (default behavior).

## CSV conversion

No CSV conversion script is included in this repository. If you need `.csv`
files, convert externally using a streaming reader to avoid large memory spikes.
