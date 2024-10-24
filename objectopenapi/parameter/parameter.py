from copy import deepcopy
import os
from typing import Any, Literal, Optional, TypeAlias
from objectopenapi.example.example import Example
from objectopenapi.media_type.media_type import MediaType
from objectopenapi.reference.reference import Reference
from objectopenapi.schema.schema import Schema
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.utils.validator import validate_key_exact, validate_key_type


class HeaderParameter:
    _name: str

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    in_ = "header"
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

    _style: Optional[Literal["simple"]] = None

    @property
    def style(self) -> Optional[Literal["simple"]]:
        return self._style

    @style.setter
    def style(self, value: Optional[Literal["simple"]]) -> None:
        self._style = value

    _explode: Optional[bool] = None

    @property
    def explode(self) -> Optional[bool]:
        return self._explode

    @explode.setter
    def explode(self, value: Optional[bool]) -> None:
        self._explode = value

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

    _examples: Optional[dict[str, Reference | Example]] = None

    @property
    def examples(self) -> Optional[dict[str, Reference | Example]]:
        return self._examples

    @examples.setter
    def examples(self, value: Optional[dict[str, Reference | Example]]) -> None:
        self._examples = value

    _content: Optional[dict[str, MediaType]] = None

    @property
    def content(self) -> Optional[dict[str, MediaType]]:
        return self._content

    @content.setter
    def content(self, value: Optional[dict[str, MediaType]]) -> None:
        self._content = value

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
        if "style" in kwargs:
            self._style = validate_key_exact(
                "style", "simple", {"style": kwargs["style"]}
            )
        if "explode" in kwargs:
            self._explode = validate_key_type(
                "explode", bool, {"explode": kwargs["explode"]}
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
        if "content" in kwargs:
            self._content = {}
            for media_type in kwargs["content"]:
                try:
                    mt = MediaType(**kwargs["content"][media_type])
                    self._content[media_type] = mt
                except Exception as mtError:
                    raise SchemaMismatch(
                        f"Parameter (Header) content must be of instance MediaType. {mtError=} "
                    )

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
        if self.style is not None:
            source["style"] = self.style
        elif remove_unset:
            source.pop("style", None)
        if self.explode is not None:
            source["explode"] = self.explode
        elif remove_unset:
            source.pop("explode", None)
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
        if self.content is not None:
            source["content"] = {k: self.content[k].dump({}) for k in self.content}
        elif remove_unset:
            source.pop("content", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.name != value.name:
            return False
        if self.description != value.description:
            return False
        if self.required != value.required:
            return False
        if self.deprecated != value.deprecated:
            return False
        if self.allowEmptyValue != value.allowEmptyValue:
            return False
        if self.style != value.style:
            return False
        if self.explode != value.explode:
            return False
        if self.schema != value.schema:
            return False
        if self.example != value.example:
            return False
        if self.examples != value.examples:
            if set((self.examples or {}).keys()) != set((value.examples or {}).keys()):
                return False
            for key in set((self.examples or {}).keys()):
                if (self.examples or {})[key] != (value.examples or {})[key]:
                    return False

        if self.content != value.content:
            if set((self.content or {}).keys()) != set((value.content or {}).keys()):
                return False
            for key in set((self.content or {}).keys()):
                if (self.content or {})[key] != (value.content or {})[key]:
                    return False
        return True


class QueryParameter:
    _name: str

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    in_ = "query"
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

    _style: Optional[
        Literal["form"]
        | Literal["spaceDelimited"]
        | Literal["pipeDelimited"]
        | Literal["deepObject"]
    ] = None

    @property
    def style(
        self,
    ) -> Optional[
        Literal["form"]
        | Literal["spaceDelimited"]
        | Literal["pipeDelimited"]
        | Literal["deepObject"]
    ]:
        return self._style

    @style.setter
    def style(
        self,
        value: Optional[
            Literal["form"]
            | Literal["spaceDelimited"]
            | Literal["pipeDelimited"]
            | Literal["deepObject"]
        ],
    ) -> None:
        self._style = value

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

    _examples: Optional[dict[str, Reference | Example]] = None

    @property
    def examples(self) -> Optional[dict[str, Reference | Example]]:
        return self._examples

    @examples.setter
    def examples(self, value: Optional[dict[str, Reference | Example]]) -> None:
        self._examples = value

    _content: Optional[dict[str, MediaType]] = None

    @property
    def content(self) -> Optional[dict[str, MediaType]]:
        return self._content

    @content.setter
    def content(self, value: Optional[dict[str, MediaType]]) -> None:
        self._content = value

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
        if "style" in kwargs:
            self._style = validate_key_exact(
                "style",
                ["form", "spaceDelimited", "pipeDelimited", "deepObject"],
                {"style": kwargs["style"]},
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
            self._example = validate_key_type(
                "example", JSON_DICT, {"example": kwargs["example"]}
            )
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
        if "content" in kwargs:
            self._content = {}
            for media_type in kwargs["content"]:
                try:
                    mt = MediaType(**kwargs["content"][media_type])
                    self._content[media_type] = mt
                except Exception as mtError:
                    raise SchemaMismatch(
                        f"Parameter (Header) content must be of instance MediaType. {mtError=} "
                    )

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
        if self.content is not None:
            source["content"] = {k: self.content[k].dump({}) for k in self.content}
        elif remove_unset:
            source.pop("content", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.name != value.name:
            return False
        if self.description != value.description:
            return False
        if self.required != value.required:
            return False
        if self.deprecated != value.deprecated:
            return False
        if self.allowEmptyValue != value.allowEmptyValue:
            return False
        if self.style != value.style:
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
            if set((self.examples or {}).keys()) != set((value.examples or {}).keys()):
                return False
            for key in set((self.examples or {}).keys()):
                if (self.examples or {})[key] != (value.examples or {})[key]:
                    return False
        if self.content != value.content:
            if set((self.content or {}).keys()) != set((value.content or {}).keys()):
                return False
            for key in set((self.content or {}).keys()):
                if (self.content or {})[key] != (value.content or {})[key]:
                    return False
        return True


class PathParameter:
    _name: str

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    in_ = "path"
    _description: Optional[str] = None

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    required = True
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

    _style: Optional[Literal["matrix"] | Literal["label"] | Literal["simple"]] = None

    @property
    def style(
        self,
    ) -> Optional[Literal["matrix"] | Literal["label"] | Literal["simple"]]:
        return self._style

    @style.setter
    def style(
        self, value: Optional[Literal["matrix"] | Literal["label"] | Literal["simple"]]
    ) -> None:
        self._style = value

    _explode: Optional[bool] = None

    @property
    def explode(self) -> Optional[bool]:
        return self._explode

    @explode.setter
    def explode(self, value: Optional[bool]) -> None:
        self._explode = value

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

    _examples: Optional[dict[str, Reference | Example]] = None

    @property
    def examples(self) -> Optional[dict[str, Reference | Example]]:
        return self._examples

    @examples.setter
    def examples(self, value: Optional[dict[str, Reference | Example]]) -> None:
        self._examples = value

    _content: Optional[dict[str, MediaType]] = None

    @property
    def content(self) -> Optional[dict[str, MediaType]]:
        return self._content

    @content.setter
    def content(self, value: Optional[dict[str, MediaType]]) -> None:
        self._content = value

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
        if "deprecated" in kwargs:
            self._deprecated = validate_key_type(
                "deprecated", bool, {"deprecated": kwargs["deprecated"]}
            )
        if "allowEmptyValue" in kwargs:
            self._allowEmptyValue = validate_key_type(
                "allowEmptyValue", bool, {"allowEmptyValue": kwargs["allowEmptyValue"]}
            )
        if "style" in kwargs:
            self._style = validate_key_exact(
                "style",
                ["matrix", "label", "simple"],
                {"style": kwargs["style"]},
            )
        if "explode" in kwargs:
            self._explode = validate_key_type(
                "explode", bool, {"explode": kwargs["explode"]}
            )
        if "schema" in kwargs:
            self._schema = Schema(**kwargs["schema"])
        if "example" in kwargs:
            self._example = validate_key_type(
                "example", JSON_DICT, {"example": kwargs["example"]}
            )
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
        if "content" in kwargs:
            self._content = {}
            for media_type in kwargs["content"]:
                try:
                    mt = MediaType(**kwargs["content"][media_type])
                    self._content[media_type] = mt
                except Exception as mtError:
                    raise SchemaMismatch(
                        f"Parameter (Header) content must be of instance MediaType. {mtError=} "
                    )

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
        if self.deprecated is not None:
            source["deprecated"] = self.deprecated
        elif remove_unset:
            source.pop("deprecated", None)
        if self.allowEmptyValue is not None:
            source["allowEmptyValue"] = self.allowEmptyValue
        elif remove_unset:
            source.pop("allowEmptyValue", None)
        if self.style is not None:
            source["style"] = self.style
        elif remove_unset:
            source.pop("style", None)
        if self.explode is not None:
            source["explode"] = self.explode
        elif remove_unset:
            source.pop("explode", None)
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
        if self.content is not None:
            source["content"] = {k: self.content[k].dump({}) for k in self.content}
        elif remove_unset:
            source.pop("content", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.name != value.name:
            return False
        if self.description != value.description:
            return False
        if self.deprecated != value.deprecated:
            return False
        if self.allowEmptyValue != value.allowEmptyValue:
            return False
        if self.style != value.style:
            return False
        if self.explode != value.explode:
            return False
        if self.schema != value.schema:
            return False
        if self.example != value.example:
            return False
        if self.examples != value.examples:
            if set((self.examples or {}).keys()) != set((value.examples or {}).keys()):
                return False
            for key in set((self.examples or {}).keys()):
                if (self.examples or {})[key] != (value.examples or {})[key]:
                    return False
        if self.content != value.content:
            if set((self.content or {}).keys()) != set((value.content or {}).keys()):
                return False
            for key in set((self.content or {}).keys()):
                if (self.content or {})[key] != (value.content or {})[key]:
                    return False
        return True


class CookieParameter:
    _name: str

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    in_ = "cookie"
    _description: Optional[str]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    _required: Optional[bool]

    @property
    def required(self) -> Optional[bool]:
        return self._required

    @required.setter
    def required(self, value: Optional[bool]) -> None:
        self._required = value

    _deprecated: Optional[bool]

    @property
    def deprecated(self) -> Optional[bool]:
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: Optional[bool]) -> None:
        self._deprecated = value

    _allowEmptyValue: Optional[bool]

    @property
    def allowEmptyValue(self) -> Optional[bool]:
        return self._allowEmptyValue

    @allowEmptyValue.setter
    def allowEmptyValue(self, value: Optional[bool]) -> None:
        self._allowEmptyValue = value

    _style: Optional[Literal["form"]]

    @property
    def style(self) -> Optional[Literal["form"]]:
        return self._style

    @style.setter
    def style(self, value: Optional[Literal["form"]]) -> None:
        self._style = value

    _explode: Optional[bool]

    @property
    def explode(self) -> Optional[bool]:
        return self._explode

    @explode.setter
    def explode(self, value: Optional[bool]) -> None:
        self._explode = value

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

    _examples: Optional[dict[str, Reference | Example]]

    @property
    def examples(self) -> Optional[dict[str, Reference | Example]]:
        return self._examples

    @examples.setter
    def examples(self, value: Optional[dict[str, Reference | Example]]) -> None:
        self._examples = value

    _content: Optional[dict[str, MediaType]] = None

    @property
    def content(self) -> Optional[dict[str, MediaType]]:
        return self._content

    @content.setter
    def content(self, value: Optional[dict[str, MediaType]]) -> None:
        self._content = value

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
        if "style" in kwargs:
            self._style = validate_key_exact(
                "style", "form", {"style": kwargs["style"]}
            )
        if "explode" in kwargs:
            self._explode = validate_key_type(
                "explode", bool, {"explode": kwargs["explode"]}
            )
        if "schema" in kwargs:
            self._schema = Schema(**kwargs["schema"])
        if "example" in kwargs:
            self._example = validate_key_type(
                "example", JSON_DICT, {"example": kwargs["example"]}
            )
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
                            f"Parameter (Cookie) examples must be of instance Example or Reference. {exampleError=} {refError=}"
                        )
        if "content" in kwargs:
            self._content = {}
            for media_type in kwargs["content"]:
                try:
                    mt = MediaType(**kwargs["content"][media_type])
                    self._content[media_type] = mt
                except Exception as mtError:
                    raise SchemaMismatch(
                        f"Parameter (Cookie) content must be of instance MediaType. {mtError=} "
                    )

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
        if self.style is not None:
            source["style"] = self.style
        elif remove_unset:
            source.pop("style", None)
        if self.explode is not None:
            source["explode"] = self.explode
        elif remove_unset:
            source.pop("explode", None)
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
        if self.content is not None:
            source["content"] = {k: self.content[k].dump({}) for k in self.content}
        elif remove_unset:
            source.pop("content", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.name != value.name:
            return False
        if self.description != value.description:
            return False
        if self.required != value.required:
            return False
        if self.deprecated != value.deprecated:
            return False
        if self.allowEmptyValue != value.allowEmptyValue:
            return False
        if self.style != value.style:
            return False
        if self.explode != value.explode:
            return False
        if self.schema != value.schema:
            return False
        if self.example != value.example:
            return False
        if self.examples != value.examples:
            if set((self.examples or {}).keys()) != set((value.examples or {}).keys()):
                return False
            for key in set((self.examples or {}).keys()):
                if (self.examples or {})[key] != (value.examples or {})[key]:
                    return False
        if self.content != value.content:
            if set((self.content or {}).keys()) != set((value.content or {}).keys()):
                return False
            for key in set((self.content or {}).keys()):
                if (self.content or {})[key] != (value.content or {})[key]:
                    return False
        return True


Parameter: TypeAlias = (
    CookieParameter | PathParameter | HeaderParameter | QueryParameter
)


def ParseParameter(**kwargs: Any) -> "Parameter":
    in_: Literal["cookie"] | Literal["header"] | Literal["path"] | Literal["query"] = (
        kwargs["in"]
    )
    match in_:
        case "cookie":
            return CookieParameter(**kwargs)
        case "header":
            return HeaderParameter(**kwargs)
        case "path":
            return PathParameter(**kwargs)
        case "query":
            return QueryParameter(**kwargs)
    raise SchemaMismatch(f"Parameter must have a proper 'in' property is {in_}.")
