# Calendar contract and scheduling math

## Export format

`resource`, `start` and `end` are required, in any order. `status` is optional;
extra named columns (for example a planning note) are ignored. Blank or
duplicate header names and inconsistent row widths are errors. Quote values
containing a comma, quote, or newline using normal CSV rules. Truly blank
records are skipped. Input is UTF-8 with or without a BOM.

Resource labels are trimmed, nonempty printable text. Times are trimmed before
parsing. Empty/missing status means `busy`; `tentative` also blocks unless opted
out. `free` and `cancelled` do not block, but still establish a resource name.
Unknown statuses, reversed times and zero-length entries fail validation,
even for an unselected resource. A resource absent from all input files is
unknown; the program does not assume it is free.

```csv
resource,start,end,status
"Room, West",09:15,10:00,busy
Bench,09:45,10:30,tentative
```

## How the answers are computed

1. Reserve half-open intervals `[start, end)`. Pad occupied spans before/after
   and clamp to `[00:00, 24:00]`. Adjacent bookings do not overlap, but leave
   no free minute between them.
2. Sort/merge each union (work and occupied) in `O(n log n)` time. A forward
   sweep subtracts occupied spans from work spans, including across lunch or
   multiple shifts. Overlapping resource bookings never double-count minutes.
3. In a free block starting at `lo`, the first grid start is
   `lo + (anchor - lo) % step`. The **entire** duration must fit; an exact end
   fit is allowed. The grid never resets at the end of a busy interval.
4. `--near` ranks by distance from the requested **start**, earlier first on a
   tie. `--non-overlap` instead takes the earliest compatible equal-duration
   appointment. Earliest finish leaves the most remaining room, yielding the
   maximum count for that grid. `summary --duration` uses this same packing.

`rooms` and `explain` retain the original blocker labels. They test a request
against whole shifts and real overlaps, not rounded percentages. A manual
block applies to everyone. For machine output, `explain --format json` uses
`null` as the manual block's resource, and separates its padded interval from
the exact overlap. Inputs and resource labels stay local; share reports with care.
