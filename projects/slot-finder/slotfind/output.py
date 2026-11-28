import csv
import json

from .time import clock


def describe(block):
    return {"start": clock(block.start), "end": clock(block.end), "minutes": block.minutes}


def write_blocks(blocks, fmt, output):
    if fmt == "json":
        json.dump([describe(block) for block in blocks], output)
        output.write("\n")
    elif fmt == "csv":
        writer = csv.DictWriter(output, fieldnames=("start", "end", "minutes"), lineterminator="\n")
        writer.writeheader()
        writer.writerows(describe(block) for block in blocks)
    else:
        for block in blocks:
            print(block, file=output)


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
