from contextlib import contextmanager, nullcontext
import os
from pathlib import Path
import tempfile


def input_stream(path, fallback):
    """Never close a borrowed stream; preserve embedded line endings in files."""
    if path == "-":
        return nullcontext(fallback)
    return open(path, encoding="utf-8-sig", newline="")



@contextmanager
def output_stream(path, fallback, *, replace=False, input_path="-"):
    if path == "-":
        if replace:
            raise OSError("--replace needs a named output")
        yield fallback
        return
    dest = Path(path)
    if replace and dest.is_symlink():
        raise OSError("refusing to replace a symbolic link")
    if replace and input_path != "-" and dest.exists() and os.path.samefile(input_path, dest):
        raise OSError("input and output refer to the same file")
    if not replace and os.path.lexists(dest):
        raise FileExistsError(f"output already exists: {dest}")
    temp = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                                       dir=dest.parent, prefix=".csvclean-", delete=False)
    try:
        with temp:
            yield temp
        # Linking rather than renaming makes the no-clobber check atomic.
        if replace:
            os.replace(temp.name, dest)
        else:
            os.link(temp.name, dest)
    finally:
        Path(temp.name).unlink(missing_ok=True)


@contextmanager
def field_limit(characters):
    """Temporarily override the csv module's process-wide character limit."""
    import csv
    from .layout import OptionError
    if characters is None:
        yield
        return
    try:
        previous = csv.field_size_limit(characters)
    except OverflowError as exc:
        raise OptionError("field limit exceeds the platform maximum") from exc
    try:
        yield
    finally:
        csv.field_size_limit(previous)
