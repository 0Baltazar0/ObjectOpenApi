from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.reference.reference import Reference
from objectopenapi.response.response import Response
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.utils.validator import validate_key_type


class Responses:
    _default: Response | Reference

    @property
    def default(self) -> Response | Reference:
        return self._default

    @default.setter
    def default(self, value: Response | Reference) -> None:
        self._default = value

    _others: Optional[dict[str, Response | Reference]]

    @property
    def others(self) -> Optional[dict[str, Response | Reference]]:
        return self._others

    @others.setter
    def others(self, value: Optional[dict[str, Response | Reference]]) -> None:
        self._others = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "default" in kwargs:
            self._default = validate_key_type(
                "default", Response | Reference, {"default": kwargs["default"]}
            )
        else:
            raise SchemaMismatch(
                'Object must contain "default" value (Response | Reference)'
            )
        self.others = {}
        for others_key in kwargs:
            if others_key == "default" or others_key.startswith("x-"):
                continue
            others_errors = []
            try:
                response_entry = Response(**kwargs[others_key])
                self.others[others_key] = response_entry
                continue
            except Exception as Response_error:
                others_errors.append(
                    f"__CLASS__ others instance failed on parsing Response: {Response_error}"
                )
            try:
                reference_entry = Reference(**kwargs[others_key])
                self.others[others_key] = reference_entry
                continue
            except Exception as Reference_error:
                others_errors.append(
                    f"__CLASS__ others instance failed on parsing Reference: {Reference_error}"
                )
            raise SchemaMismatch(
                f"__CLASS__ others parse failed on the following error list:{chr(92)}{f'{chr(92)}'.join(others_errors)}"
            )

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        source["default"] = self.default.dump({})
        if self.others is not None:
            others = {k: self.others[k].dump({}) for k in self.others}
            source.update(others)
        elif remove_unset:
            source.pop("others", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.default != value.default:
            return False
        if (
            value.others
            and self.others
            and set(self.others.keys()) == set(value.others.keys())
        ):
            for key in self.others:
                if value.others[key] != self.others[key]:
                    return False
        elif self.others or value.others:
            return False
        return True
