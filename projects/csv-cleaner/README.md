# CSV cleaner

A streaming reader for checking and cleaning delimited tables without loading
the whole file. It understands quoted separators and multiline records, and
keeps the original line range for diagnostics. Requires Python 3.9+; no install.

From this directory:

```sh
python3 -m unittest discover -s tests
```

In Python, call `csvclean.reader.records(stream)` on a text file opened with
`newline=""`. Each result has `first`, `last` and `fields` attributes.

From the shell: `python3 -m csvclean validate < input.csv`. It reports the
number of data rows and columns, or exits with status 1 and a line diagnostic.
