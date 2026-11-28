import csv

from .transform import CellEdits
from .layout import compile_layout
from .reader import check_width, read_header, records


def clean_table(source, target, *, delimiter=",", skip_blank=False, output_delimiter=",", edits=CellEdits(), trim_header=False, keep=(), drop=(), rename=()):
    rows = records(source, delimiter, skip_blank=skip_blank)
    header = read_header(rows, trim=trim_header)
    # CRLF also makes the standard writer quote cells containing a bare CR.
    writer = csv.writer(target, delimiter=output_delimiter, lineterminator="\r\n")
    layout = compile_layout(header, keep=keep, drop=drop, rename=rename)
    writer.writerow(layout.names)
    for row in rows:
        check_width(row, header)
        values = edits.apply(layout.select(row.fields))
        if values is not None:
            writer.writerow(values)
