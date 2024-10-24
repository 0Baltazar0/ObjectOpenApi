from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.header.header import Header
from objectopenapi.link.link import Link
from objectopenapi.media_type.media_type import MediaType
from objectopenapi.reference.reference import Reference
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.utils.validator import validate_key_type


class Response:
    _description: str

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    _headers: Optional[dict[str, Header | Reference]]

    @property
    def headers(self) -> Optional[dict[str, Header | Reference]]:
        return self._headers

    @headers.setter
    def headers(self, value: Optional[dict[str, Header | Reference]]) -> None:
        self._headers = value

    _content: Optional[dict[str, MediaType]]

    @property
    def content(self) -> Optional[dict[str, MediaType]]:
        return self._content

    @content.setter
    def content(self, value: Optional[dict[str, MediaType]]) -> None:
        self._content = value

    _links: Optional[dict[str, Link | Reference]]

    @property
    def links(self) -> Optional[dict[str, Link | Reference]]:
        return self._links

    @links.setter
    def links(self, value: Optional[dict[str, Link | Reference]]) -> None:
        self._links = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "description" in kwargs:
            self._description = validate_key_type(
                "description", str, {"description": kwargs["description"]}
            )
        else:
            raise SchemaMismatch('Object must contain "description" value (str)')
        if "headers" in kwargs:
            self.headers = {}
            for headers_key in kwargs["headers"]:
                headers_errors = []
                try:
                    header_entry = Header(**kwargs["headers"][headers_key])
                    self.headers[headers_key] = header_entry
                    continue
                except Exception as Header_error:
                    headers_errors.append(
                        f"__CLASS__ headers instance failed on parsing Header: {Header_error}"
                    )
                try:
                    reference_entry = Reference(**kwargs["headers"][headers_key])
                    self.headers[headers_key] = reference_entry
                    continue
                except Exception as Reference_error:
                    headers_errors.append(
                        f"__CLASS__ headers instance failed on parsing Reference: {Reference_error}"
                    )
                raise SchemaMismatch(
                    f"__CLASS__ headers parse failed on the following error list:{chr(92)} {f'{chr(92)}'.join(headers_errors)}"
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
        if "links" in kwargs:
            self.links = {}
            for link_key in kwargs["links"]:
                link_errors = []
                try:
                    reference_entry = Reference(**kwargs["links"][link_key])
                    self.links[link_key] = reference_entry
                    continue
                except Exception as Reference_error:
                    link_errors.append(
                        f"__CLASS__ links instance failed on parsing Reference: {Reference_error}"
                    )
                try:
                    link_entry = Link(**kwargs["links"][link_key])
                    self.links[link_key] = link_entry
                    continue
                except Exception as Link_error:
                    link_errors.append(
                        f"__CLASS__ links instance failed on parsing Link: {Link_error}"
                    )
                raise SchemaMismatch(
                    f"__CLASS__ links parse failed on the following error list:{chr(92)} {f'{chr(92)}'.join(link_errors)}"
                )

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        source["description"] = self.description
        if self.headers is not None:
            source["headers"] = {k: self.headers[k].dump({}) for k in self.headers}
        elif remove_unset:
            source.pop("headers", None)
        if self.content is not None:
            source["content"] = {k: self.content[k].dump({}) for k in self.content}
        elif remove_unset:
            source.pop("content", None)
        if self.links is not None:
            source["links"] = {k: self.links[k].dump({}) for k in self.links}
        elif remove_unset:
            source.pop("links", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.description != value.description:
            return False
        if (
            self.headers
            and value.headers
            and set(self.headers.keys()) == set(value.headers.keys())
        ):
            for key in self.headers:
                if value.headers[key] != self.headers[key]:
                    return False
        elif self.headers != value.headers:
            return False
        if (
            self.content
            and value.content
            and set(self.content.keys()) == set(value.content.keys())
        ):
            for key in self.content:
                if value.content[key] != self.content[key]:
                    return False
        elif self.content != value.content:
            return False
        if (
            self.links
            and value.links
            and set(self.links.keys()) == set(value.links.keys())
        ):
            for key in self.links:
                if value.links[key] != self.links[key]:
                    return False
        else:
            return False
        return True
