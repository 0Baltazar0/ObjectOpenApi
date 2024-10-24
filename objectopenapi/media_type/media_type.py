from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.encoding.encoding import Encoding
from objectopenapi.example.example import Example
from objectopenapi.reference.reference import Reference
from objectopenapi.schema.schema import Schema
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch


class MediaType:
    _schema: Optional[Schema]

    @property
    def schema(self) -> Optional[Schema]:
        return self._schema

    @schema.setter
    def schema(self, value: Optional[Schema]) -> None:
        self._schema = value

    _example: Optional[JSON_DICT]

    @property
    def example(self) -> Optional[JSON_DICT]:
        return self._example

    @example.setter
    def example(self, value: Optional[JSON_DICT]) -> None:
        self._example = value

    _examples: Optional[dict[str, Example | Reference]]

    @property
    def examples(self) -> Optional[dict[str, Example | Reference]]:
        return self._examples

    @examples.setter
    def examples(self, value: Optional[dict[str, Example | Reference]]) -> None:
        self._examples = value

    _encoding: Optional[dict[str, Encoding]]

    @property
    def encoding(self) -> Optional[dict[str, Encoding]]:
        return self._encoding

    @encoding.setter
    def encoding(self, value: Optional[dict[str, Encoding]]) -> None:
        self._encoding = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
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
        if "encoding" in kwargs:
            self._encoding = {}
            for encoding in kwargs["content"]:
                try:
                    en = Encoding(**kwargs["content"][encoding])
                    self._encoding[encoding] = en
                except Exception as enError:
                    raise SchemaMismatch(
                        f"Parameter (Header) content must be of instance MediaType. {enError=} "
                    )

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
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
        if self.encoding is not None:
            source["encoding"] = {k: self.encoding[k].dump({}) for k in self.encoding}
        elif remove_unset:
            source.pop("encoding", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.schema != value.schema:
            return False
        if self.example != value.example:
            return False
        if self.examples != value.examples:
            return False
        if self.encoding != value.encoding:
            return False
        return True
