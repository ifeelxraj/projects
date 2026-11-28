# CSV cleaner

Validate an incoming table, understand its missing values, and write a cleaned
copy without loading the dataset into memory. No install, network access, or
third-party packages. Use Python 3.9 or later.

## Try it

```sh
cd projects/csv-cleaner
./csv-clean validate examples/stock.scsv --delimiter semicolon --schema examples/stock.schema.json
./csv-clean profile examples/stock.scsv --delimiter semicolon --only note
make demo
make test
```

`make demo` runs the [stock recipe](examples/stock-recipe.sh). Three messy stock
rows become two numbered rows; `03` stays `03`. Run `python3 -m csvclean` from
the project directory as an alternative to the launcher. Use `--help` after any
subcommand to see its flags.

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
