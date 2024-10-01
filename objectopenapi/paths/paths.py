import os
from typing import Any, Optional
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch


class PathItem:
    _ref: Optional[str]

    @property
    def ref(self) -> Optional[str]:
        return self._ref

    @ref.setter
    def ref(self, value: Optional[str]) -> None:
        self._ref = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "ref" in kwargs:
            self._ref = kwargs["ref"]

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = self.source

        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        if self._ref:
            source["ref"] = self._ref
        elif remove_unset:
            source.pop("ref", None)
        return source

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, PathItem):
            return False

        if value.ref != self.ref:
            return False

        return True


class Paths:
    _paths: dict[str, PathItem]

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        for item in kwargs:
            if not isinstance(kwargs[item], dict):
                raise SchemaMismatch(
                    f"Paths must contain path items, and each path item must be a dict (is {type(kwargs[item])})"
                )
            self._paths[item] = PathItem(**kwargs[item])

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        if not source and not remove_unset:
            source = self.source
        source = {p: self._paths[p].dump({}) for p in self._paths}
        return source

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Paths):
            return False

        self_set = set(self._paths.keys())
        val_set = set(value._paths.keys())

        if val_set != self_set:
            return False

        for key in val_set:
            if self._paths[key] != value._paths[key]:
                return False
        return True
