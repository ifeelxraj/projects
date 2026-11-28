#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
exec ./csv-clean clean examples/stock.scsv --delimiter semicolon \
  --schema examples/stock.schema.json --trim --keep item --keep quantity --keep note \
  --rename quantity units --fill-empty unknown --collapse-adjacent --number-rows seq --summary
