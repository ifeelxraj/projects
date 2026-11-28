# Slot finder

Find a time when all selected resources are free, or find an individual room
that can host a particular meeting. It reads local files only: no account,
calendar API, timezone conversion or booking side effects. Python 3.9+, no install.

```sh
cd projects/slot-finder
./find-slots free --window 09:00-12:00 --busy 10:00-10:30
make demo
make test
```

The demo reads [a fictional shared morning](examples/shared-morning.csv) and
returns two 30-minute alternatives nearest 10:00: **10:00–10:30** and
**09:45–10:15**. Overlap between alternatives is intentional. Use
`--non-overlap` instead of `--near` to build an actual sequence of appointments.
The launcher also works from another directory; `python3 -m slotfind` works
from the project root. Each command has its own `--help`.

## Queries

| Command | Question |
| --- | --- |
| `free [--min 30m]` | Which maximal free blocks meet the minimum length? |
| `slots --duration 30m` | Which fixed-length meetings fit? `--step` sets start spacing (default 15m); `--anchor HH:MM` sets the grid phase. `--limit N` is applied **after** ranking or packing. |
| `summary [--duration 30m]` | How many working minutes are occupied/free? With a duration, how many nonoverlapping grid-aligned meetings really fit? |
| `explain START-END` | Is the entire requested interval inside work hours and free? Show the intersecting resource/manual blocks, including buffers. |
| `rooms START-END` | Which individual resources can host the **whole** request? Two rooms free for half each are not a match. |

```sh
./find-slots rooms 10:30-11:00 --calendar examples/shared-morning.csv
./find-slots explain 10:25-10:30 --before 5m --calendar examples/shared-morning.csv
./find-slots summary --window 09:00-12:00 --calendar examples/shared-morning.csv --duration 30m --format json
```

## Inputs and outputs

- Default work hours are `09:00-17:00`. Repeat `--window` for split shifts and
  `--busy` for manual blocks that apply to **every** resource.
- Repeat `--calendar FILE` for UTF-8 booking CSVs; `--calendar -` reads stdin
  once. Use `--resource NAME` to select one or more exact labels across files.
  Unrecognized names are errors, not silently free calendars.
- `--before` and `--after` buffer each booking. `--ignore-tentative` changes
  the default conservative policy. Durations accept `90`, `90m`, `1h`, `1h30m`.
- Intervals stay within **one local day**. Use two-digit `HH:MM` and half-open
  ranges; `24:00` is a valid end. Split overnight work into separate days.
- `--format text|json|csv` controls result format (`explain`: text/JSON only).
  No results is normally success: empty text, `[]`, or a header-only CSV.
  `--require-match` on `free`, `slots` or `rooms` returns status `3` instead.
  Status `1` means malformed calendar data; `2` means bad arguments, encoding,
  unknown resource or unreadable input. Diagnostics use stderr.
