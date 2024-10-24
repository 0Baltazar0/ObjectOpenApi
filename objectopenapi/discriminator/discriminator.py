from copy import deepcopy
import os
from typing import Any, Optional

from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.utils.validator import validate_key_type


class Discriminator:
    _propertyName: str

    @property
    def propertyName(self) -> str:
        return self._propertyName

    @propertyName.setter
    def propertyName(self, value: str) -> None:
        self._propertyName = value

    _mapping: Optional[dict[str, str]]

    @property
    def mapping(self) -> Optional[dict[str, str]]:
        return self._mapping

    @mapping.setter
    def mapping(self, value: Optional[dict[str, str]]) -> None:
        self._mapping = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "propertyName" in kwargs:
            self._propertyName = validate_key_type(
                "propertyName", str, {"propertyName": kwargs["propertyName"]}
            )
        else:
            raise SchemaMismatch('Object must contain "propertyName" value (str)')
        if "mapping" in kwargs:
            self._mapping = validate_key_type(
                "mapping", dict[str, str], {"mapping": kwargs["mapping"]}
            )

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        source["propertyName"] = self.propertyName
        if self.mapping is not None:
            source["mapping"] = self.mapping  # type:ignore
        elif remove_unset:
            source.pop("mapping", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.propertyName != value.propertyName:
            return False
        if self.mapping != value.mapping:
            return False
        return True
