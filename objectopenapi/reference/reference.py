from copy import deepcopy
import os
from typing import Any, Optional

from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.utils.validator import validate_key_type


class Reference:
    _ref: str

    @property
    def ref(self) -> str:
        return self._ref

    @ref.setter
    def ref(self, value: str) -> None:
        self._ref = value

    _summary: Optional[str] = None

    @property
    def summary(self) -> Optional[str]:
        return self._summary

    @summary.setter
    def summary(self, value: Optional[str]) -> None:
        self._summary = value

    _description: Optional[str] = None

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "$ref" in kwargs:
            self._ref = validate_key_type("ref", str, {"ref": kwargs["$ref"]})
        else:
            raise SchemaMismatch('Object must contain "$ref" value (str)')
        if "summary" in kwargs:
            self._summary = validate_key_type(
                "summary", str, {"summary": kwargs["summary"]}
            )
        if "description" in kwargs:
            self._description = validate_key_type(
                "description", str, {"description": kwargs["description"]}
            )

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        source["$ref"] = self.ref
        if self.summary is not None:
            source["summary"] = self.summary
        elif remove_unset:
            source.pop("summary", None)
        if self.description is not None:
            source["description"] = self.description
        elif remove_unset:
            source.pop("description", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.ref != value.ref:
            return False
        if self.summary != value.summary:
            return False
        if self.description != value.description:
            return False
        return True
