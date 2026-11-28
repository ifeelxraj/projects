# Small projects

Each project lives in `projects/` and has its own setup instructions.

| Project | What it does | Stack | Status |
| --- | --- | --- | --- |
| [ATM simulator](projects/atm-simulator/) | Practice deposits, withdrawals and reconciliation against a ten-entry mini-statement. | C++17 | Complete |
| [CSV cleaner](projects/csv-cleaner/) | Validate and clean delimited tables without loading them into memory. | Python | Complete |
| [Slot finder](projects/slot-finder/) | Find shared free time in a local working day. | Python | Complete |

## Try the simulator

```sh
make -C projects/atm-simulator demo   # replay a sample account session
make -C projects/atm-simulator test   # run unit and terminal tests
```

The simulator replaces the original top-level `atm system.cpp`. See its
[guide](projects/atm-simulator/README.md) to build it, start an interactive
session, or configure a withdrawal allowance.

## Try the CSV cleaner

```sh
make -C projects/csv-cleaner demo
```

The [CSV guide](projects/csv-cleaner/README.md) covers validation, profiling,
cleaning order and atomic output files.

## Find an available meeting time

```sh
projects/slot-finder/slot-finder free --window 09:00-12:00 --busy 10:00-10:30
python3 examples/availability/csv_cleaner_to_slot_finder.py
```

The [slot finder](projects/slot-finder/README.md) can find shared blocks, rank
meeting suggestions, and explain conflicts. The [export-to-slots recipe](examples/availability/)
combines both Python tools without producing a schedule from a partial import.
Run `make demo` at the root to replay all examples.

## Continue development

Run `python3 tools/projects_daily_brief.py` for the current index, recent history and daily
handoffs. The [contributor guide](CONTRIBUTING.md) explains the check, commit,
stop and logging process. Dated run notes live in `logs/`.

Run `make test` at the repository root to check the catalog, contributor tools,
and all completed projects together.
