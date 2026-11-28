# Small projects

Each project lives in `projects/` and has its own setup instructions.

| Project | What it does | Stack | Status |
| --- | --- | --- | --- |
| [ATM simulator](projects/atm-simulator/) | Practice deposits, withdrawals and reconciliation against a ten-entry mini-statement. | C++17 | Complete |
| [CSV cleaner](projects/csv-cleaner/) | Validate and clean delimited tables without loading them into memory. | Python | Complete |

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

## Continue development

Run `python3 tools/run_brief.py` for the current index, recent history and daily
handoffs. The [contributor guide](CONTRIBUTING.md) explains the check, commit,
stop and logging process. Dated run notes live in `logs/`.
