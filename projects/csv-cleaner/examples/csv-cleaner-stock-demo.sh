#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
exec ./csv-cleaner clean examples/csv-cleaner-stock.scsv --delimiter semicolon \
  --schema examples/csv-cleaner-stock.schema.json --trim --keep item --keep quantity --keep note \
  --rename quantity units --fill-empty unknown --collapse-adjacent --number-rows seq --summary
