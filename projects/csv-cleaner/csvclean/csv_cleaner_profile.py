"""Profile shape and completeness without collecting or exposing cell values."""

from .csv_cleaner_columns import compile_layout
from .csv_cleaner_reader import Table


def profile(source, *, only=(), **options):
    table = Table(source, **options)
    layout = compile_layout(table.header, keep=only)
    columns = [{"name": name, "empty": 0, "whitespace_only": 0, "max_chars": 0} for name in layout.names]
    count = 0
    for row in table:
        count += 1
        for cell, stats in zip(layout.select(row.fields), columns):
            if not cell:
                stats["empty"] += 1
            elif not cell.strip():
                stats["whitespace_only"] += 1
            stats["max_chars"] = max(stats["max_chars"], len(cell))
    return {"rows": count, "columns": columns}
