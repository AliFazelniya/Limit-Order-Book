set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="${ROOT_DIR}/data"

if ! command -v unxz >/dev/null 2>&1; then
  echo "unxz command not found. Install xz-utils first." >&2
  exit 1
fi

if [ ! -d "${DATA_DIR}" ]; then
  echo "Data directory not found at ${DATA_DIR}" >&2
  exit 1
fi

find "${DATA_DIR}" -type f -name '*.xz' -print0 | while IFS= read -r -d '' file; do
  echo "Decompressing ${file}"
  unxz -k "${file}"
done
