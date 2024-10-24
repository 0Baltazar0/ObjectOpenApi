from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.validator import validate_key_type


class Example:
    _summary: Optional[str]

    @property
    def summary(self) -> Optional[str]:
        return self._summary

    @summary.setter
    def summary(self, value: Optional[str]) -> None:
        self._summary = value

    _description: Optional[str]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    _value: Optional[JSON_DICT]

    @property
    def value(self) -> Optional[JSON_DICT]:
        return self._value

    @value.setter
    def value(self, value: Optional[JSON_DICT]) -> None:
        self._value = value

    _externalValue: Optional[str]

    @property
    def externalValue(self) -> Optional[str]:
        return self._externalValue

    @externalValue.setter
    def externalValue(self, value: Optional[str]) -> None:
        self._externalValue = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "summary" in kwargs:
            self._summary = validate_key_type(
                "summary", str, {"summary": kwargs["summary"]}
            )
        if "description" in kwargs:
            self._description = validate_key_type(
                "description", str, {"description": kwargs["description"]}
            )
        if "value" in kwargs:
            self._value = kwargs["value"]
        if "externalValue" in kwargs:
            self._externalValue = validate_key_type(
                "externalValue", str, {"externalValue": kwargs["externalValue"]}
            )

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        if self.summary is not None:
            source["summary"] = self.summary
        elif remove_unset:
            source.pop("summary", None)
        if self.description is not None:
            source["description"] = self.description
        elif remove_unset:
            source.pop("description", None)
        if self.value is not None:
            source["value"] = self.value
        elif remove_unset:
            source.pop("value", None)
        if self.externalValue is not None:
            source["externalValue"] = self.externalValue
        elif remove_unset:
            source.pop("externalValue", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.summary != value.summary:
            return False
        if self.description != value.description:
            return False
        if self.value != value.value:
            return False
        if self.externalValue != value.externalValue:
            return False
        return True
