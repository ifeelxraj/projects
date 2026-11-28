# From a room export to meeting slots

This example uses **two** projects: CSV cleaner reads the original booking table,
then Slot finder works out which meeting times are still free.

From the repository root, run:

```sh
python3 examples/availability/csv_cleaner_to_slot_finder.py
```

It validates the [fictional TSV export](csv-cleaner-to-slot-finder-bookings.tsv), renames its columns into
the calendar contract and returns two feasible starts: **10:30** and **11:30**.
Pass a different export (or `-` for stdin), `--window`, or `--duration` to reuse
it. The output is a JSON array. Input data is never edited.

The intermediate CSV lives in a temporary directory and is published only when
cleaning succeeds. This matters: an ordinary shell pipe could let a planner
produce suggestions from a truncated export even if the upstream command fails.
