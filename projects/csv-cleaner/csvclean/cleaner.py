import csv

from .transform import CellEdits
from .layout import OptionError, compile_layout
from .reader import Table


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
    written = 0
    previous = None
    for row in table:
        values = edits.apply(layout.select(row.fields))
        if values is None or (collapse and values == previous):
            continue
        written += 1
        writer.writerow((written, *values) if number_rows is not None else values)
        if collapse:
            previous = values
