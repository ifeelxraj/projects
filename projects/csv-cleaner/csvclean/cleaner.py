import csv

from .reader import check_width, read_header, records


def clean_table(source, target, *, delimiter=",", skip_blank=False, output_delimiter=","):
    rows = records(source, delimiter, skip_blank=skip_blank)
    header = read_header(rows)
    # CRLF also makes the standard writer quote cells containing a bare CR.
    writer = csv.writer(target, delimiter=output_delimiter, lineterminator="\r\n")
    writer.writerow(header)
    for row in rows:
        check_width(row, header)
        writer.writerow(row.fields)
