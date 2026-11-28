# Slot finder

Give it working hours and a list of bookings. It shows when everyone is free,
or which room can host a meeting at a time you choose. It reads local files;
it does not connect to a calendar, make reservations or convert time zones.
Python 3.9+, no install.

```sh
cd projects/slot-finder
./slot-finder free --window 09:00-12:00 --busy 10:00-10:30
make demo
make test
```

The demo reads [a fictional shared morning](examples/slot-finder-morning-bookings.csv) and
returns two 30-minute alternatives nearest 10:00: **10:00–10:30** and
**09:45–10:15**. Overlap between alternatives is intentional. Use
`--non-overlap` instead of `--near` to build an actual sequence of appointments.
The launcher also works from another directory; `python3 -m slotfind` works
from the project root. Each command has its own `--help`.

The runnable file is now named `slot-finder` (previously `find-slots`). The
`make` targets, `python3 -m slotfind`, and command options are unchanged.

## Where to start reading

To see how a 30-minute meeting gets suggested, start with **free time**: the
planner first removes booked minutes, then tries possible meeting starts in
the gaps that remain.

| File | What it does |
| --- | --- |
| [slot-finder](slot-finder) → [slot_finder_commands.py](slotfind/slot_finder_commands.py) | Starts the program and handles questions like `free`, `slots` and `rooms`. |
| [slot_finder_calendar_reader.py](slotfind/slot_finder_calendar_reader.py) | Reads the room names and booking times from a calendar CSV. |
| [slot_finder_time_ranges.py](slotfind/slot_finder_time_ranges.py) | Converts `09:15` to minutes and represents a start/end pair. |
| [slot_finder_free_time.py](slotfind/slot_finder_free_time.py) | Subtracts booked periods from working hours. |
| [slot_finder_meeting_slots.py](slotfind/slot_finder_meeting_slots.py) | Finds meeting starts that fit completely inside a free block. |
| [slot_finder_schedule.py](slotfind/slot_finder_schedule.py) | Brings working hours, rooms and bookings together to answer queries. |
| [slot_finder_output.py](slotfind/slot_finder_output.py) | Prints the answers as text, JSON or CSV. |

The [examples](examples/) contain sample bookings and a command to try. The
[tests](tests/) are named `test_slot_finder_` plus the feature they check.

## Queries

| Command | Question |
| --- | --- |
| `free [--min 30m]` | Which maximal free blocks meet the minimum length? |
| `slots --duration 30m` | Which fixed-length meetings fit? `--step` sets start spacing (default 15m); `--anchor HH:MM` sets the grid phase. `--limit N` is applied **after** ranking or packing. |
| `summary [--duration 30m]` | How many working minutes are occupied/free? With a duration, how many nonoverlapping grid-aligned meetings really fit? |
| `explain START-END` | Is the entire requested interval inside work hours and free? Show the intersecting resource/manual blocks, including buffers. |
| `rooms START-END` | Which individual resources can host the **whole** request? Two rooms free for half each are not a match. |

```sh
./slot-finder rooms 10:30-11:00 --calendar examples/slot-finder-morning-bookings.csv
./slot-finder explain 10:25-10:30 --before 5m --calendar examples/slot-finder-morning-bookings.csv
./slot-finder summary --window 09:00-12:00 --calendar examples/slot-finder-morning-bookings.csv --duration 30m --format json
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

See [Calendar contract and scheduling math](slot-finder-calendar-guide.md) for import details, boundary rules and ranking.
