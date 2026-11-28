# CSV cleaner

Give it a table saved as a CSV file, like a spreadsheet of shop stock. It can
spot a row with missing columns, remove unwanted spaces, and write a cleaned
copy. It reads one row at a time. Use Python 3.9 or later; no install or network
connection is needed.

## Try it

```sh
cd projects/csv-cleaner
./csv-cleaner validate examples/csv-cleaner-stock.scsv --delimiter semicolon --schema examples/csv-cleaner-stock.schema.json
./csv-cleaner profile examples/csv-cleaner-stock.scsv --delimiter semicolon --only note
make demo
make test
```

`make demo` runs the [stock recipe](examples/csv-cleaner-stock-demo.sh). Three messy stock
rows become two numbered rows; `03` stays `03`. Run `python3 -m csvclean` from
the project directory as an alternative to the launcher. Use `--help` after any
subcommand to see its flags.

The runnable file is now named `csv-cleaner` (previously `csv-clean`). The
`make` targets, `python3 -m csvclean`, and command options are unchanged.

## Where to start reading

To follow one row from input to output, open the **reader**, then the **pipeline**.

| File | What it does |
| --- | --- |
| [csv-cleaner](csv-cleaner) → [csv_cleaner_commands.py](csvclean/csv_cleaner_commands.py) | Starts the program and decides whether to check, clean or describe your table. |
| [csv_cleaner_reader.py](csvclean/csv_cleaner_reader.py) | Reads rows, checks the header and reports which lines are malformed. |
| [csv_cleaner_pipeline.py](csvclean/csv_cleaner_pipeline.py) | Sends each checked row through the requested edits and writes it out. |
| [csv_cleaner_columns.py](csvclean/csv_cleaner_columns.py) / [csv_cleaner_cell_edits.py](csvclean/csv_cleaner_cell_edits.py) | Choose and rename columns; trim spaces or fill empty cells. |
| [csv_cleaner_value_rules.py](csvclean/csv_cleaner_value_rules.py) / [csv_cleaner_schema.py](csvclean/csv_cleaner_schema.py) | Check values, such as dates, and load those checks from a reusable rule file. |
| [csv_cleaner_profile.py](csvclean/csv_cleaner_profile.py) | Counts empty cells and measures text lengths without displaying private values. |
| [csv_cleaner_file_io.py](csvclean/csv_cleaner_file_io.py) | Opens files and publishes the finished output only after validation. |

The [examples](examples/) are sample stock data, its rules and the demo command.
Files under [tests](tests/) beginning with `test_csv_cleaner_` check the feature
named in the rest of the filename; they aren't extra programs to run.

## Commands

| Command | Output |
| --- | --- |
| `validate [FILE]` | Count data rows and columns, or report input line ranges. `--max-errors N` can collect multiple bad rows. `--json` emits the report on stdout even for invalid data. |
| `clean [FILE]` | Canonical quoted CSV with CRLF record endings. No sorting or type conversion. Named output is published only after all rows pass. |
| `profile [FILE]` | JSON row count and, per column, empty count, whitespace-only count, and maximum length in Unicode code points. No cell samples. |
| `schema [FILE]` | A starter JSON rule file using the header only; this is **not** a data validation pass. |

Omit `FILE` or use `-` for stdin. Named files and pipes are UTF-8, with an
optional initial BOM. `--delimiter` and `--output-delimiter` take `comma`, `tab`,
`semicolon`, or `pipe`; nothing is guessed. Use `--skip-blank` for empty records:
it does not skip `""`, and a row consisting of delimiters still has fields.

## Cleaning order

1. Read and check the header. `--trim-header` strips names **before** duplicate
   checks. Header names are otherwise literal and case-sensitive.
2. Validate every input row and its rules, even columns that will be dropped.
3. Project with repeated `--keep NAME` in output order, or `--drop NAME` in
   original order. `--rename OLD NEW` operates simultaneously on retained names.
4. Apply `--trim`, then `--skip-empty` across projected cells, then `--fill-empty TEXT`.
5. `--collapse-adjacent` compares consecutive **emitted** values, not all prior
   rows. Finally `--number-rows NAME` prepends contiguous one-based numbers.

`--summary` writes the examined, skipped, collapsed and written counts to stderr
on success. CSV stays on stdout or in `-o FILE`. Cleaning does not make text
safe to execute or interpret as formulas in a spreadsheet.

## Output and failure guarantees

- `-o FILE` defaults to no overwrite. A sibling temporary file is linked into
  place atomically; the destination filesystem must support hard links.
- `--replace -o FILE` explicitly allows replacement after validation. It refuses
  the named input, schema file, their aliases, and symbolic-link destinations.
  The replacement is a new file; old permissions/metadata are not copied.
- Stdout is a stream: it can contain a valid prefix on failure. **Do not** use
  shell redirection back onto the input; the shell truncates before startup.
- Status `0` means success, `1` invalid CSV/data, `2` usage, configuration,
  encoding or I/O error. `--field-limit CHARS` bounds a single parsed field;
  otherwise Python's CSV parser limit applies. Memory depends on record width,
  maximum record size and the configured diagnostic limit, not total row count.

For the rule grammar, key ordering and JSON report contract, see [Validating a data contract](csv-cleaner-schema-guide.md).
