from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.header.header import Header
from objectopenapi.reference.reference import Reference
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.utils.validator import validate_key_type


class Encoding:
    _contentType: Optional[str]

    @property
    def contentType(self) -> Optional[str]:
        return self._contentType

    @contentType.setter
    def contentType(self, value: Optional[str]) -> None:
        self._contentType = value

    _headers: Optional[dict[str, Header | Reference]]

    @property
    def headers(self) -> Optional[dict[str, Header | Reference]]:
        return self._headers

    @headers.setter
    def headers(self, value: Optional[dict[str, Header | Reference]]) -> None:
        self._headers = value

    _style: Optional[str]

    @property
    def style(self) -> Optional[str]:
        return self._style

    @style.setter
    def style(self, value: Optional[str]) -> None:
        self._style = value

    _explode: Optional[bool]

    @property
    def explode(self) -> Optional[bool]:
        return self._explode

    @explode.setter
    def explode(self, value: Optional[bool]) -> None:
        self._explode = value

    _allowReserved: Optional[bool]

    @property
    def allowReserved(self) -> Optional[bool]:
        return self._allowReserved

    @allowReserved.setter
    def allowReserved(self, value: Optional[bool]) -> None:
        self._allowReserved = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "contentType" in kwargs:
            self._contentType = validate_key_type(
                "contentType", str, {"contentType": kwargs["contentType"]}
            )
        if "headers" in kwargs:
            self._headers = {}
            for header in kwargs["headers"]:
                try:
                    ex = Header(**kwargs["headers"][header])
                    self._headers[header] = ex
                    continue
                except Exception as headerError:
                    try:
                        ref = Reference(**kwargs["headers"][header])
                        self._headers[header] = ref
                    except Exception as refError:
                        raise SchemaMismatch(
                            f"Encoding 'header' must be of instance Header or Reference. {headerError=} {refError=}"
                        )

        if "style" in kwargs:
            self._style = validate_key_type("style", str, {"style": kwargs["style"]})
        if "explode" in kwargs:
            self._explode = validate_key_type(
                "explode", bool, {"explode": kwargs["explode"]}
            )
        if "allowReserved" in kwargs:
            self._allowReserved = validate_key_type(
                "allowReserved", bool, {"allowReserved": kwargs["allowReserved"]}
            )

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        if self.contentType is not None:
            source["contentType"] = self.contentType
        elif remove_unset:
            source.pop("contentType", None)
        if self.headers is not None:
            source["headers"] = {k: self.headers[k].dump({}) for k in self.headers}
        elif remove_unset:
            source.pop("headers", None)
        if self.style is not None:
            source["style"] = self.style
        elif remove_unset:
            source.pop("style", None)
        if self.explode is not None:
            source["explode"] = self.explode
        elif remove_unset:
            source.pop("explode", None)
        if self.allowReserved is not None:
            source["allowReserved"] = self.allowReserved
        elif remove_unset:
            source.pop("allowReserved", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.contentType != value.contentType:
            return False
        if self.headers != value.headers:
            return False
        if self.style != value.style:
            return False
        if self.explode != value.explode:
            return False
        if self.allowReserved != value.allowReserved:
            return False
        return True
