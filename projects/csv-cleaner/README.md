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
