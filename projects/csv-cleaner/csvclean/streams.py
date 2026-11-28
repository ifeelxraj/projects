from contextlib import nullcontext


def input_stream(path, fallback):
    """Never close a borrowed stream; preserve embedded line endings in files."""
    if path == "-":
        return nullcontext(fallback)
    return open(path, encoding="utf-8-sig", newline="")
