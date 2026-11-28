from contextlib import nullcontext


def input_stream(path, fallback):
    """Never close a borrowed stream; preserve embedded line endings in files."""
    if path == "-":
        return nullcontext(fallback)
    return open(path, encoding="utf-8-sig", newline="")


from contextlib import contextmanager
import os
from pathlib import Path
import tempfile


@contextmanager
def output_stream(path, fallback):
    if path == "-":
        yield fallback
        return
    dest = Path(path)
    if os.path.lexists(dest):
        raise FileExistsError(f"output already exists: {dest}")
    temp = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                                       dir=dest.parent, prefix=".csvclean-", delete=False)
    try:
        with temp:
            yield temp
        # Linking rather than renaming makes the no-clobber check atomic.
        os.link(temp.name, dest)
    finally:
        Path(temp.name).unlink(missing_ok=True)
