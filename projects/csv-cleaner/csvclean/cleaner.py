import csv

from .reader import check_width, read_header, records


def clean_table(source, target, *, delimiter=",", skip_blank=False, output_delimiter=",", trim=False, trim_header=False):
    rows = records(source, delimiter, skip_blank=skip_blank)
    header = read_header(rows, trim=trim_header)
    # CRLF also makes the standard writer quote cells containing a bare CR.
    writer = csv.writer(target, delimiter=output_delimiter, lineterminator="\r\n")
    writer.writerow(header)
    for row in rows:
        check_width(row, header)
        values = tuple(cell.strip() for cell in row.fields) if trim else row.fields
        writer.writerow(values)
