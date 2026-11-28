# Validating a data contract

Create a starting point from the header, then add only the constraints the
consumer actually needs:

```sh
./csv-clean schema examples/stock.scsv --delimiter semicolon
./csv-clean validate examples/stock.scsv --delimiter semicolon \
  --schema examples/stock.schema.json --max-errors 8 --json
```

The [example contract](examples/stock.schema.json) declares the following keys.
The JSON object must have integer `version: 1`. Unknown keys, duplicate keys and
duplicate names in a list are errors, not warnings.

| Key | Meaning |
| --- | --- |
| `columns` | Optional nonempty list pinning the exact header names **and order**. Omit to allow extra columns. |
| `required` | Named cells must contain something besides whitespace. |
| `integer` | Optional sign followed by ASCII digits. Leading zeroes remain intact. |
| `decimal` | Optional sign, ASCII digits, and optionally a point followed by digits. No exponent, NaN, locale separators or rounding. |
| `date` | Real calendar date in exactly `YYYY-MM-DD` form. |

Type checks allow an empty cell unless it is also required. They check the
original cell, **not** a trimmed or default-filled result. CLI rules (`--require`,
`--integer`, `--decimal`, `--date`) add to file rules. A missing required column
in the rule configuration is an option error; a header differing from an
explicit `columns` contract is a data error.

For pre-sorted feeds use repeated `--order-by NAME` in key priority order;
`--strict-order` also forbids equal adjacent keys. Keys are tuples of original
text, not inferred numbers: `10` sorts before `2`. The checker does not reorder
records or keep a set of every key. It compares successive structurally valid,
cell-rule-passing records.

`validate --json` reports `examined` logical data rows, `columns`, `issues` and
`stopped`. Each issue contains `first_line`, `last_line`, and `message`. At most
one issue is reported per bad row. `stopped` means the error cap was reached or
a header/parse error made continuation impossible; it does not assert that
unread records contain additional errors. A malformed unfinished record has no
completed data row to count. Configuration and I/O failures go to stderr.
