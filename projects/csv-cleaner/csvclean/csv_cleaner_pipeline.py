import csv
from dataclasses import dataclass

from .csv_cleaner_cell_edits import CellEdits
from .csv_cleaner_columns import OptionError, compile_layout
from .csv_cleaner_reader import Table


@dataclass
class Counts:
    examined: int = 0
    written: int = 0
    empty_skipped: int = 0
    collapsed: int = 0


def clean_table(source, target, *, output_delimiter=",", edits=CellEdits(),
                keep=(), drop=(), rename=(), collapse=False, number_rows=None, **options):
    table = Table(source, **options)
    # CRLF also makes the standard writer quote cells containing a bare CR.
    writer = csv.writer(target, delimiter=output_delimiter, lineterminator="\r\n")
    layout = compile_layout(table.header, keep=keep, drop=drop, rename=rename)
    labels = layout.names
    if number_rows is not None:
        if not number_rows.strip() or number_rows in labels:
            raise OptionError("row number needs a new nonblank output column name")
        labels = (number_rows, *labels)
    writer.writerow(labels)
    counts = Counts()
    previous = None
    for row in table:
        counts.examined += 1
        values = edits.apply(layout.select(row.fields))
        if values is None:
            counts.empty_skipped += 1
            continue
        if collapse and values == previous:
            counts.collapsed += 1
            continue
        counts.written += 1
        writer.writerow((counts.written, *values) if number_rows is not None else values)
        if collapse:
            previous = values
    return counts
