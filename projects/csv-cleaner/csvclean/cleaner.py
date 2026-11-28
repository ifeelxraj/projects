import csv

from .transform import CellEdits
from .layout import compile_layout
from .reader import Table


def clean_table(source, target, *, output_delimiter=",", edits=CellEdits(),
                keep=(), drop=(), rename=(), collapse=False, **options):
    table = Table(source, **options)
    # CRLF also makes the standard writer quote cells containing a bare CR.
    writer = csv.writer(target, delimiter=output_delimiter, lineterminator="\r\n")
    layout = compile_layout(table.header, keep=keep, drop=drop, rename=rename)
    writer.writerow(layout.names)
    previous = None
    for row in table:
        values = edits.apply(layout.select(row.fields))
        if values is None or (collapse and values == previous):
            continue
        writer.writerow(values)
        if collapse:
            previous = values
