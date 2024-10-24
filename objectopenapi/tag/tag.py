from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.external_doc.external_doc import ExternalDocs
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.utils.validator import validate_key_type


class Tag:
    _name: str

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    _description: Optional[str]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    _externalDocs: Optional[ExternalDocs]

    @property
    def externalDocs(self) -> Optional[ExternalDocs]:
        return self._externalDocs

    @externalDocs.setter
    def externalDocs(self, value: Optional[ExternalDocs]) -> None:
        self._externalDocs = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "name" in kwargs:
            self._name = validate_key_type("name", str, {"name": kwargs["name"]})
        else:
            raise SchemaMismatch('Object must contain "name" value (str)')
        if "description" in kwargs:
            self._description = validate_key_type(
                "description", str, {"description": kwargs["description"]}
            )
        if "externalDocs" in kwargs:
            self._externalDocs = ExternalDocs(**kwargs["externalDocs"])

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        source["name"] = self.name
        if self.description is not None:
            source["description"] = self.description
        elif remove_unset:
            source.pop("description", None)
        if self.externalDocs is not None:
            source["externalDocs"] = self.externalDocs.dump({})
        elif remove_unset:
            source.pop("externalDocs", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.name != value.name:
            return False
        if self.description != value.description:
            return False
        if self.externalDocs != value.externalDocs:
            return False
        return True
