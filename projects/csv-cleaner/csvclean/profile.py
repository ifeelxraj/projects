"""Profile shape and completeness without collecting or exposing cell values."""

from .reader import Table


def profile(source, **options):
    table = Table(source, **options)
    columns = [{"name": name, "empty": 0, "whitespace_only": 0, "max_chars": 0} for name in table.header]
    count = 0
    for row in table:
        count += 1
        for cell, stats in zip(row.fields, columns):
            if not cell:
                stats["empty"] += 1
            elif not cell.strip():
                stats["whitespace_only"] += 1
            stats["max_chars"] = max(stats["max_chars"], len(cell))
    return {"rows": count, "columns": columns}
