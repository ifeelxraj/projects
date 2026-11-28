import json

from .time import clock


def describe(block):
    return {"start": clock(block.start), "end": clock(block.end), "minutes": block.minutes}


def write_blocks(blocks, fmt, output):
    if fmt == "json":
        json.dump([describe(block) for block in blocks], output)
        output.write("\n")
    else:
        for block in blocks:
            print(block, file=output)
