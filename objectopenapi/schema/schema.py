from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.discriminator.discriminator import Discriminator
from objectopenapi.external_documentation.external_documentation import (
    ExternalDocumentation,
)
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.xml.xml import XML
from objectopenapi.data_types.types import TypeDeclaration, parse_type


class Schema:
    _json_type: TypeDeclaration

    @property
    def json_type(self) -> TypeDeclaration:
        return self._json_type

    @json_type.setter
    def json_type(self, value: Any) -> None:
        self._json_type = parse_type(value)

    _discriminator: Optional[Discriminator]

    @property
    def discriminator(self) -> Optional[Discriminator]:
        return self._discriminator

    @discriminator.setter
    def discriminator(self, value: Optional[Discriminator]) -> None:
        self._discriminator = value

    _xml: Optional[XML]

    @property
    def xml(self) -> Optional[XML]:
        return self._xml

    @xml.setter
    def xml(self, value: Optional[XML]) -> None:
        self._xml = value

    _externalDocs: Optional[ExternalDocumentation]

    @property
    def externalDocs(self) -> Optional[ExternalDocumentation]:
        return self._externalDocs

    @externalDocs.setter
    def externalDocs(self, value: Optional[ExternalDocumentation]) -> None:
        self._externalDocs = value

    _example: Optional[JSON_DICT]

    @property
    def example(self) -> Optional[JSON_DICT]:
        return self._example

    @example.setter
    def example(self, value: Optional[JSON_DICT]) -> None:
        self._example = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "discriminator" in kwargs:
            self._discriminator = Discriminator(**kwargs["discriminator"])
        if "xml" in kwargs:
            self._xml = XML(**kwargs["xml"])
        if "externalDocs" in kwargs:
            self._externalDocs = ExternalDocumentation(**kwargs["externalDocs"])
        if "example" in kwargs:
            self._example = kwargs["example"]

        type_source: Any = deepcopy(kwargs)
        type_source.pop("discriminator", "")
        type_source.pop("xml", "")
        type_source.pop("externalDocs", "")
        type_source.pop("example", "")
        self.json_type = type_source

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        source.update(self.json_type.dump({}))
        if self.discriminator is not None:
            source["discriminator"] = self.discriminator.dump({})
        elif remove_unset:
            source.pop("discriminator", None)
        if self.xml is not None:
            source["xml"] = self.xml.dump({})
        elif remove_unset:
            source.pop("xml", None)
        if self.externalDocs is not None:
            source["externalDocs"] = self.externalDocs.dump({})
        elif remove_unset:
            source.pop("externalDocs", None)
        if self.example is not None:
            source["example"] = self.example
        elif remove_unset:
            source.pop("example", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.discriminator != value.discriminator:
            return False
        if self.xml != value.xml:
            return False
        if self.externalDocs != value.externalDocs:
            return False
        if self.example != value.example:
            return False
        return True
