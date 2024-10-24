from copy import deepcopy
import os
from typing import Any, Optional

from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.validator import validate_key_type


class XML:
    _name: Optional[str]

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        self._name = value

    _namespace: Optional[str]

    @property
    def namespace(self) -> Optional[str]:
        return self._namespace

    @namespace.setter
    def namespace(self, value: Optional[str]) -> None:
        self._namespace = value

    _prefix: Optional[str]

    @property
    def prefix(self) -> Optional[str]:
        return self._prefix

    @prefix.setter
    def prefix(self, value: Optional[str]) -> None:
        self._prefix = value

    _attribute: Optional[bool]

    @property
    def attribute(self) -> Optional[bool]:
        return self._attribute

    @attribute.setter
    def attribute(self, value: Optional[bool]) -> None:
        self._attribute = value

    _wrapped: Optional[bool]

    @property
    def wrapped(self) -> Optional[bool]:
        return self._wrapped

    @wrapped.setter
    def wrapped(self, value: Optional[bool]) -> None:
        self._wrapped = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "name" in kwargs:
            self._name = validate_key_type("name", str, {"name": kwargs["name"]})
        if "namespace" in kwargs:
            self._namespace = validate_key_type(
                "namespace", str, {"namespace": kwargs["namespace"]}
            )
        if "prefix" in kwargs:
            self._prefix = validate_key_type(
                "prefix", str, {"prefix": kwargs["prefix"]}
            )
        if "attribute" in kwargs:
            self._attribute = validate_key_type(
                "attribute", bool, {"attribute": kwargs["attribute"]}
            )
        if "wrapped" in kwargs:
            self._wrapped = validate_key_type(
                "wrapped", bool, {"wrapped": kwargs["wrapped"]}
            )

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        if self.name is not None:
            source["name"] = self.name
        elif remove_unset:
            source.pop("name", None)
        if self.namespace is not None:
            source["namespace"] = self.namespace
        elif remove_unset:
            source.pop("namespace", None)
        if self.prefix is not None:
            source["prefix"] = self.prefix
        elif remove_unset:
            source.pop("prefix", None)
        if self.attribute is not None:
            source["attribute"] = self.attribute
        elif remove_unset:
            source.pop("attribute", None)
        if self.wrapped is not None:
            source["wrapped"] = self.wrapped
        elif remove_unset:
            source.pop("wrapped", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.name != value.name:
            return False
        if self.namespace != value.namespace:
            return False
        if self.prefix != value.prefix:
            return False
        if self.attribute != value.attribute:
            return False
        if self.wrapped != value.wrapped:
            return False
        return True
