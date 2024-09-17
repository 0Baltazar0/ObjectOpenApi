from typing import Any


def merge_dict(*dicts: dict[str, Any]) -> dict[str, Any]:
    dd: dict[str, Any] = {}
    for d in dicts:
        dd.update(d)
    return dd
