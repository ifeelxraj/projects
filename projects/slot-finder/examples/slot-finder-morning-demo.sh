#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
exec ./slot-finder slots --window 09:00-12:00 --calendar examples/slot-finder-morning-bookings.csv \
  --duration 30m --step 15m --near 10:00 --limit 2 --format json --require-match
