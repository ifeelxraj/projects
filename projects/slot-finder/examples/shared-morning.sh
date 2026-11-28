#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
exec ./find-slots slots --window 09:00-12:00 --calendar examples/shared-morning.csv \
  --duration 30m --step 15m --near 10:00 --limit 2 --format json --require-match
