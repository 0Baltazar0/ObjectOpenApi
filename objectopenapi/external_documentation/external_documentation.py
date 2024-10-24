from copy import deepcopy
import os
from typing import Any, Optional

from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.utils.validator import validate_key_type


class ExternalDocumentation:
    _description: Optional[str]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    _url: str

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        self._url = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "description" in kwargs:
            self._description = validate_key_type(
                "description", str, {"description": kwargs["description"]}
            )
        if "url" in kwargs:
            self._url = validate_key_type("url", str, {"url": kwargs["url"]})
        else:
            raise SchemaMismatch('Object must contain "url" value (str)')

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        if self.description is not None:
            source["description"] = self.description
        elif remove_unset:
            source.pop("description", None)
        source["url"] = self.url
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.description != value.description:
            return False
        if self.url != value.url:
            return False
        return True
