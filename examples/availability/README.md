# From a room export to meeting slots

Run `python3 examples/availability/plan_export.py` from the repository root.
It validates the [fictional TSV export](vendor.tsv), renames its columns into
the calendar contract and returns two feasible starts: **10:30** and **11:30**.
Pass a different export (or `-` for stdin), `--window`, or `--duration` to reuse
it. The output is a JSON array. Input data is never edited.

The intermediate CSV lives in a temporary directory and is published only when
cleaning succeeds. This matters: an ordinary shell pipe could let a planner
produce suggestions from a truncated export even if the upstream command fails.
