from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.media_type.media_type import MediaType
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.utils.validator import validate_key_type


class RequestBody:
    _description: Optional[str]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    _content: dict[str, MediaType]

    @property
    def content(self) -> dict[str, MediaType]:
        return self._content

    @content.setter
    def content(self, value: dict[str, MediaType]) -> None:
        self._content = value

    _required: Optional[bool]

    @property
    def required(self) -> Optional[bool]:
        return self._required

    @required.setter
    def required(self, value: Optional[bool]) -> None:
        self._required = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "description" in kwargs:
            self._description = validate_key_type(
                "description", str, {"description": kwargs["description"]}
            )
        if "content" in kwargs:
            self.content = {}
            for content_key in kwargs["content"]:
                try:
                    self.content[content_key] = MediaType(
                        **kwargs["content"][content_key]
                    )
                except Exception as content_error:
                    raise SchemaMismatch(
                        f"__CLASS__ content instance must be of type MediaType,{content_error:}"
                    )
        else:
            raise SchemaMismatch(
                'Object must contain "content" value ((str, MediaType))'
            )
        if "required" in kwargs:
            self._required = validate_key_type(
                "required", bool, {"required": kwargs["required"]}
            )

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
        source["content"] = {k: self.content[k].dump({}) for k in self.content}
        if self.required is not None:
            source["required"] = self.required
        elif remove_unset:
            source.pop("required", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.description != value.description:
            return False
        if set(self.content.keys()) == set(value.content.keys()):
            for key in self.content:
                if value.content[key] != self.content[key]:
                    return False
        else:
            return False
        if self.required != value.required:
            return False
        if set(self.content.keys()) == set(value.content.keys()):
            for key in self.content:
                if value.content[key] != self.content[key]:
                    return False
        else:
            return False
        return True
