from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.example.example import Example
from objectopenapi.reference.reference import Reference
from objectopenapi.schema.schema import Schema
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.utils.validator import validate_key_type


class Header:
    _description: Optional[str] = None

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    _required: Optional[bool] = None

    @property
    def required(self) -> Optional[bool]:
        return self._required

    @required.setter
    def required(self, value: Optional[bool]) -> None:
        self._required = value

    _deprecated: Optional[bool] = None

    @property
    def deprecated(self) -> Optional[bool]:
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: Optional[bool]) -> None:
        self._deprecated = value

    _allowEmptyValue: Optional[bool] = None

    @property
    def allowEmptyValue(self) -> Optional[bool]:
        return self._allowEmptyValue

    @allowEmptyValue.setter
    def allowEmptyValue(self, value: Optional[bool]) -> None:
        self._allowEmptyValue = value

    style = "simple"
    _explode: Optional[bool] = None

    @property
    def explode(self) -> Optional[bool]:
        return self._explode

    @explode.setter
    def explode(self, value: Optional[bool]) -> None:
        self._explode = value

    _allowReserved: Optional[bool] = None

    @property
    def allowReserved(self) -> Optional[bool]:
        return self._allowReserved

    @allowReserved.setter
    def allowReserved(self, value: Optional[bool]) -> None:
        self._allowReserved = value

    _schema: Optional[Schema] = None

    @property
    def schema(self) -> Optional[Schema]:
        return self._schema

    @schema.setter
    def schema(self, value: Optional[Schema]) -> None:
        self._schema = value

    _example: Optional[JSON_DICT] = None

    @property
    def example(self) -> Optional[JSON_DICT]:
        return self._example

    @example.setter
    def example(self, value: Optional[JSON_DICT]) -> None:
        self._example = value

    _examples: Optional[dict[str, Example | Reference]] = None

    @property
    def examples(self) -> Optional[dict[str, Example | Reference]]:
        return self._examples

    @examples.setter
    def examples(self, value: Optional[dict[str, Example | Reference]]) -> None:
        self._examples = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "description" in kwargs:
            self._description = validate_key_type(
                "description", str, {"description": kwargs["description"]}
            )
        if "required" in kwargs:
            self._required = validate_key_type(
                "required", bool, {"required": kwargs["required"]}
            )
        if "deprecated" in kwargs:
            self._deprecated = validate_key_type(
                "deprecated", bool, {"deprecated": kwargs["deprecated"]}
            )
        if "allowEmptyValue" in kwargs:
            self._allowEmptyValue = validate_key_type(
                "allowEmptyValue", bool, {"allowEmptyValue": kwargs["allowEmptyValue"]}
            )
        if "explode" in kwargs:
            self._explode = validate_key_type(
                "explode", bool, {"explode": kwargs["explode"]}
            )
        if "allowReserved" in kwargs:
            self._allowReserved = validate_key_type(
                "allowReserved", bool, {"allowReserved": kwargs["allowReserved"]}
            )
        if "schema" in kwargs:
            self._schema = Schema(**kwargs["schema"])
        if "example" in kwargs:
            self._example = kwargs["example"]
        if "examples" in kwargs:
            self._examples = {}
            for example in kwargs["examples"]:
                try:
                    ex = Example(**kwargs["examples"][example])
                    self._examples[example] = ex
                    continue
                except Exception as exampleError:
                    try:
                        ref = Reference(**kwargs["examples"][example])
                        self._examples[example] = ref
                    except Exception as refError:
                        raise SchemaMismatch(
                            f"Parameter (Header) examples must be of instance Example or Reference. {exampleError=} {refError=}"
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
        if self.required is not None:
            source["required"] = self.required
        elif remove_unset:
            source.pop("required", None)
        if self.deprecated is not None:
            source["deprecated"] = self.deprecated
        elif remove_unset:
            source.pop("deprecated", None)
        if self.allowEmptyValue is not None:
            source["allowEmptyValue"] = self.allowEmptyValue
        elif remove_unset:
            source.pop("allowEmptyValue", None)
        if self.explode is not None:
            source["explode"] = self.explode
        elif remove_unset:
            source.pop("explode", None)
        if self.allowReserved is not None:
            source["allowReserved"] = self.allowReserved
        elif remove_unset:
            source.pop("allowReserved", None)
        if self.schema is not None:
            source["schema"] = self.schema.dump({})
        elif remove_unset:
            source.pop("schema", None)
        if self.example is not None:
            source["example"] = self.example
        elif remove_unset:
            source.pop("example", None)
        if self.examples is not None:
            source["examples"] = {k: self.examples[k].dump({}) for k in self.examples}
        elif remove_unset:
            source.pop("examples", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.description != value.description:
            return False
        if self.required != value.required:
            return False
        if self.deprecated != value.deprecated:
            return False
        if self.allowEmptyValue != value.allowEmptyValue:
            return False
        if self.explode != value.explode:
            return False
        if self.allowReserved != value.allowReserved:
            return False
        if self.schema != value.schema:
            return False
        if self.example != value.example:
            return False
        if self.examples != value.examples:
            if self.examples is None or value.examples is None:
                return False
            if set(self.examples.keys()) != set(value.examples.keys()):
                return False
            for key in self.examples.keys():
                if self.examples[key] != value.examples[key]:
                    return False
        return True
