import csv
import json

from .slot_finder_time_ranges import clock


def describe(block):
    return {"start": clock(block.start), "end": clock(block.end), "minutes": block.minutes}


def write_blocks(blocks, fmt, output):
    if fmt == "json":
        rows = [describe(block) for block in blocks]
        print(json.dumps(rows), file=output)
        return len(rows)
    writer = None
    if fmt == "csv":
        writer = csv.DictWriter(output, fieldnames=("start", "end", "minutes"), lineterminator="\n")
        writer.writeheader()
    count = 0
    for block in blocks:
        if writer is None:
            print(block, file=output)
        else:
            writer.writerow(describe(block))
        count += 1
    return count


def write_summary(summary, fmt, output):
    if fmt == "json":
        print(json.dumps(summary), file=output)
    elif fmt == "csv":
        writer = csv.DictWriter(output, fieldnames=tuple(summary), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    else:
        for name, value in summary.items():
            print(f"{name.replace('_', ' ')}: {value}", file=output)


def write_explanation(info, fmt, output):
    if fmt == "json":
        print(json.dumps(info, ensure_ascii=False), file=output)
        return
    print(f"{info['request']}: {'available' if info['available'] else 'unavailable'}", file=output)
    if not info["inside_work"]:
        print("Not wholly inside working hours.", file=output)
    for conflict in info["conflicts"]:
        label = conflict["resource"] or "(manual block)"
        print(f"{label}: {conflict['blocked']} overlaps {conflict['overlap']}", file=output)


def write_names(names, fmt, output):
    if fmt == "json":
        print(json.dumps(names, ensure_ascii=False), file=output)
    elif fmt == "csv":
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(["resource"])
        writer.writerows([name] for name in names)
    else:
        for name in names:
            print(name, file=output)
