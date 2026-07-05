#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(dirname "$0")/..
echo "Validating Pine files..."
FAILED=0
while IFS= read -r -d '' file; do
  echo "Checking $file"
  if ! grep -q "@version=5" "$file"; then
    echo "ERROR: $file missing @version=5"
    FAILED=1
  fi
  if ! grep -q -E "indicator\(|strategy\(" "$file"; then
    echo "ERROR: $file missing indicator(...) or strategy(...) declaration"
    FAILED=1
  fi
done < <(find "$ROOT_DIR/pine" -name "*.pine" -print0)

if [ "$FAILED" -ne 0 ]; then
  echo "Pine validation failed"
  exit 2
fi

echo "Pine validation passed"
