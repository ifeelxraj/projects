"""A small, versioned JSON format for reusable column checks."""

import json

from .layout import OptionError
from .rules import Rules


RULE_KEYS = ("required", "integer", "decimal", "date")


def load_schema(path):
    try:
        with open(path, encoding="utf-8-sig") as stream:
            data = json.load(stream)
    except json.JSONDecodeError as exc:
        raise OptionError(f"schema line {exc.lineno}: {exc.msg}") from exc
    if not isinstance(data, dict) or type(data.get("version")) is not int or data["version"] != 1:
        raise OptionError("schema must be an object with version 1")
    unknown = set(data).difference(("version", "columns", *RULE_KEYS))
    if unknown:
        raise OptionError(f"unknown schema key: {min(unknown)!r}")
    result = {}
    for key in ("columns", *RULE_KEYS):
        names = data.get(key, [])
        if not isinstance(names, list) or any(not isinstance(n, str) or not n.strip() for n in names):
            raise OptionError(f"schema {key!r} must be a list of nonblank column names")
        if len(names) != len(set(names)):
            raise OptionError(f"duplicate name in schema {key!r}")
        if key == "columns" and key in data and not names:
            raise OptionError("schema columns must not be empty")
        result[key] = tuple(names)
    return result


def rules_for(args):
    values = load_schema(args.schema) if args.schema else {}
    for name, flag in (("required", "require"), ("integer", "integer"), ("decimal", "decimal"), ("date", "date")):
        values[name] = (*values.get(name, ()), *getattr(args, flag))
    return Rules(**values)
