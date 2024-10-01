from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch


class ServerVariable:
    _enum: Optional[list[str]]

    @property
    def enum(self) -> Optional[list[str]]:
        return self._enum

    @enum.setter
    def enum(self, value: Optional[list[str]]) -> None:
        self._enum = value

    _default: str

    @property
    def default(self) -> str:
        return self._default

    @default.setter
    def default(self, value: str) -> None:
        self._default = value

    _description: Optional[str]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "enum" in kwargs:
            self._enum = kwargs["enum"]
        if "default" in kwargs:
            self._default = kwargs["default"]
        else:
            raise SchemaMismatch(
                "Object document must contain a 'default' value ( str)"
            )
        if "description" in kwargs:
            self._description = kwargs["description"]

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        if self._enum:
            source["enum"] = self._enum  # type:ignore
        elif remove_unset:
            source.pop("enum", None)

        source["default"] = self._default

        if self._description:
            source["description"] = self._description
        elif remove_unset:
            source.pop("description", None)

        return source


class Server:
    _url: str

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        self._url = value

    _description: Optional[str]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    _variables: Optional[dict[str, ServerVariable]]

    @property
    def variables(self) -> Optional[dict[str, ServerVariable]]:
        return self._variables

    @variables.setter
    def variables(self, value: Optional[dict[str, ServerVariable]]) -> None:
        self._variables = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs

        if "url" in kwargs:
            self._url = kwargs["url"]
        else:
            raise SchemaMismatch("Object document must contain a 'url' value ( str)")
        if "description" in kwargs:
            self._description = kwargs["description"]
        if "variables" in kwargs:
            self._variables = kwargs["variables"]

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)

        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        source["url"] = self._url

        if self._description:
            source["description"] = self._description
        elif remove_unset:
            source.pop("description", None)

        if self._variables:
            source["variables"] = {
                k: self._variables[k].dump({}) for k in self._variables.keys()
            }
        elif remove_unset:
            source.pop("variables", None)

        return source
