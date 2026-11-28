# Slot finder

A local, single-day availability calculator. Work in minutes rather than
floating-point hours; `24:00` means the end of the day, not tomorrow's schedule.
Requires Python 3.9+ and no external packages.

From this directory, run `python3 -m unittest discover -s tests`. In Python,
`slotfind.time.minute("09:15")` gives `555`; `clock(555)` formats it again.

Try `python3 -m slotfind free --window 09:00-12:00 --busy 10:00-10:30`.
The command prints one available interval per line.
