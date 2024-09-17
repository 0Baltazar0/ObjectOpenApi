from typing import Any, Generic, Literal, Optional, TypeVar, TypeAlias

from .parse_errors import SchemaMismatch

from .common_types import JSON_DICT

from .validator import (
    is_value_type,
    validate_key_exact,
    validate_key_type,
    validate_key_type_lambda,
)

T = TypeVar("T", int, float, float | int)


def un_type(d: Any) -> Any:
    return d


class CommonKeys:
    _nullable: Optional[bool] = None
    _title: Optional[str] = None

    def __init__(self, **kwargs: Any) -> None:
        print(f"CommonKeys {kwargs}")
        if "nullable" in kwargs:
            self.nullable = kwargs["nullable"]
        if "title" in kwargs:
            self.title = kwargs["title"]

    @property
    def nullable(self) -> bool | None:
        return self._nullable

    @nullable.setter
    def nullable(self, value: Any) -> None:
        self._nullable = validate_key_type(
            "nullable", [bool, type(None)], {"nullable": value}
        )

    @property
    def title(self) -> str | None:
        return self._title

    @title.setter
    def title(self, value: Any) -> None:
        self._title = validate_key_type("title", [str, type(None)], {"title": value})

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        if self.nullable is not None:
            dest["nullable"] = self.nullable
        if self.title is not None:
            dest["title"] = self.title
        return dest

    def __eq__(self, value: object) -> bool:
        nullable = self.nullable == getattr(value, "nullable", None)
        title = self.title == getattr(value, "title", None)
        return nullable and title


class MinMaxLength:
    _minLength: Optional[int] = None
    _maxLength: Optional[int] = None

    def __init__(self, **kwargs: Any) -> None:
        if "minLength" in kwargs:
            self.minLength = kwargs.get("minLength")
        if "maxLength" in kwargs:
            self.maxLength = kwargs.get("maxLength")

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        if self.minLength:
            dest["minLength"] = self.minLength
        if self.maxLength:
            dest["maxLength"] = self.maxLength
        return dest

    @property
    def minLength(self) -> int | None:
        return self._minLength

    @minLength.setter
    def minLength(self, value: Any) -> None:
        self._minLength = validate_key_type(
            "minLength", [int, type(None)], {"minLength": value}
        )

    @property
    def maxLength(self) -> int | None:
        return self._maxLength

    @maxLength.setter
    def maxLength(self, value: Any) -> None:
        self._maxLength = validate_key_type(
            "maxLength", [int, type(None)], {"maxLength": value}
        )

    def __eq__(self, value: object) -> bool:
        minLength = self.minLength == getattr(value, "minLength", None)
        maxLength = self.maxLength == getattr(value, "maxLength", None)
        return minLength and maxLength


class BooleanType(CommonKeys):
    _default: Optional[bool] = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        if "default" in kwargs:
            self.default = kwargs["default"]

    @property
    def type(self) -> Literal["boolean"]:
        return "boolean"

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        if self.default is not None:
            dest["default"] = self.default

        super().dump(dest)
        dest["type"] = self.type
        return dest

    @property
    def default(self) -> bool | None:
        return self._default

    @default.setter
    def default(self, value: Any) -> None:
        self._default = validate_key_type(
            "default", [bool, type(None)], {"default": value}
        )

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BooleanType):
            return False
        return self.default == value.default and super().__eq__(value)


class FileType(CommonKeys):
    _format: Literal["base64"] | Literal["binary"]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.format = kwargs["format"]

    @property
    def type(self) -> Literal["string"]:
        return "string"

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        if self.format is not None:
            dest["format"] = self.format

        super().dump(dest)
        dest["type"] = self.type
        return dest

    @property
    def format(self) -> Literal["base64"] | Literal["binary"]:
        return self._format

    @format.setter
    def format(self, value: Any) -> None:
        self._format = validate_key_exact(
            "format", ["base64", "binary"], {"format": value}
        )

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, FileType):
            return False
        return self._format == value._format and super().__eq__(value)


class NumberRules(Generic[T]):
    _exclusiveMinimum: Optional[bool] = None

    @property
    def exclusiveMinimum(self) -> Optional[bool]:
        return self._exclusiveMinimum

    @exclusiveMinimum.setter
    def exclusiveMinimum(self, value: Any) -> None:
        self._exclusiveMinimum = validate_key_type(
            "value", [bool, type(None)], {"value": value}
        )

    _exclusiveMaximum: Optional[bool] = None

    @property
    def exclusiveMaximum(self) -> Optional[bool]:
        return self._exclusiveMaximum

    @exclusiveMaximum.setter
    def exclusiveMaximum(self, value: Any) -> None:
        self._exclusiveMaximum = validate_key_type(
            "value", [bool, type(None)], {"value": value}
        )

    _maximum: Optional[T] = None

    @property
    def maximum(self) -> Optional[T]:
        return self._maximum

    @maximum.setter
    def maximum(self, value: Any) -> None:
        self._maximum = validate_key_type(
            "value", [int, self.number_type, type(None)], {"value": value}
        )

    _minimum: Optional[T] = None

    @property
    def minimum(self) -> Optional[T]:
        return self._minimum

    @minimum.setter
    def minimum(self, value: Any) -> None:
        self._minimum = validate_key_type(
            "value", [int, self.number_type, type(None)], {"value": value}
        )

    _multipleOf: Optional[T] = None

    @property
    def multipleOf(self) -> Optional[T]:
        return self._multipleOf

    @multipleOf.setter
    def multipleOf(self, value: Any) -> None:
        self._multipleOf = validate_key_type(
            "value", [int, self.number_type, type(None)], {"value": value}
        )

    _number_type: Any | list[Any]

    def __init__(self, **kwargs: Any) -> None:
        self.number_type = kwargs["number_type"]
        if "exclusiveMinimum" in kwargs:
            self.exclusiveMinimum = kwargs["exclusiveMinimum"]
        if "exclusiveMaximum" in kwargs:
            self.exclusiveMaximum = kwargs["exclusiveMaximum"]
        if "maximum" in kwargs:
            self.maximum = kwargs["maximum"]
        if "minimum" in kwargs:
            self.minimum = kwargs["minimum"]
        if "multipleOf" in kwargs:
            self.multipleOf = kwargs["multipleOf"]

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        if self.exclusiveMinimum is not None:
            dest["exclusiveMinimum"] = self.exclusiveMinimum
        if self.exclusiveMaximum is not None:
            dest["exclusiveMaximum"] = self.exclusiveMaximum
        if self.maximum is not None:
            dest["maximum"] = self.maximum
        if self.minimum is not None:
            dest["minimum"] = self.minimum
        if self.multipleOf is not None:
            dest["multipleOf"] = self.multipleOf
        return dest

    def __eq__(self, value: object) -> bool:
        return (
            True
            if self.exclusiveMinimum == getattr(value, "exclusiveMinimum", None)
            and self.exclusiveMaximum == getattr(value, "exclusiveMaximum", None)
            and self.maximum == getattr(value, "maximum", None)
            and self.minimum == getattr(value, "minimum", None)
            and self.multipleOf == getattr(value, "multipleOf", None)
            else False
        )


class IntegerType(NumberRules[int | float], CommonKeys):
    _format: Literal["int32"] | Literal["int64"] | None = None

    def __init__(self, **kwargs: Any) -> None:
        NumberRules.__init__(self, number_type=float, **kwargs)
        CommonKeys.__init__(self, number_type=float, **kwargs)
        if "format" in kwargs:
            self.format = validate_key_exact("format", ["int32", "int64"], kwargs)

    @property
    def type(self) -> Literal["integer"]:
        return "integer"

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        NumberRules.dump(self, dest)
        CommonKeys.dump(self, dest)
        if self.format:
            dest["format"] = self.format
        dest["type"] = self.type
        return dest

    @property
    def format(self) -> Literal["int32"] | Literal["int64"] | None:
        return self._format

    @format.setter
    def format(self, value: Any) -> None:
        self._format = validate_key_exact(
            "format", ["int32", "int64", None], {"format": value}
        )

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, IntegerType):
            return False
        return (
            self.format == value.format
            and NumberRules.__eq__(self, value)
            and CommonKeys.__eq__(self, value)
        )


class NumberType(NumberRules[float | int], CommonKeys):
    _format: Literal["float"] | Literal["double"] | None = None

    def __init__(self, **kwargs: Any) -> None:
        if "format" in kwargs:
            self.format = validate_key_exact("format", ["double", "float"], kwargs)
        CommonKeys.__init__(self, number_type=float, **kwargs)
        NumberRules.__init__(self, number_type=float, **kwargs)

    @property
    def type(self) -> Literal["number"]:
        return "number"

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        CommonKeys.dump(self, dest)
        NumberRules.dump(self, dest)
        if self.format:
            dest["format"] = self.format
        dest["type"] = self.type
        return dest

    @property
    def format(self) -> Literal["float"] | Literal["double"] | None:
        return self._format

    @format.setter
    def format(self, value: Any) -> None:
        self._format = validate_key_exact(
            "format", ["float", "double", None], {"format": value}
        )

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, NumberType):
            return False
        return (
            self.format == value.format
            and NumberRules.__eq__(self, value)
            and CommonKeys.__eq__(self, value)
        )


class StringType(MinMaxLength, CommonKeys):
    _enum: str | list[str] | None = None

    @property
    def enum(self) -> str | list[str] | None:
        return self._enum

    @enum.setter
    def enum(self, value: Any) -> None:
        self._enum = validate_key_type("enum", [str, list, type(None)], {"enum": value})

    _format: (
        Literal["date"]
        | Literal["date-time"]
        | Literal["password"]
        | Literal["byte"]
        | Literal["binary"]
        | str
        | None
    ) = None
    _pattern: str | None = None

    @property
    def pattern(self) -> str | None:
        return self._pattern

    @pattern.setter
    def pattern(self, value: Any) -> None:
        self._pattern = validate_key_type(
            "pattern", [str, list, type(None)], {"pattern": value}
        )

    _default: str | None = None

    @property
    def default(self) -> str | None:
        return self._default

    @default.setter
    def default(self, value: Any) -> None:
        self._default = validate_key_type(
            "default", [str, list, type(None)], {"default": value}
        )

    def __init__(self, **kwargs: Any) -> None:
        MinMaxLength.__init__(self, number_type=int, **kwargs)
        CommonKeys.__init__(self, number_type=int, **kwargs)
        if "enum" in kwargs:
            self.enum = kwargs["enum"]
        if "format" in kwargs:
            self.format = kwargs["format"]
        if "pattern" in kwargs:
            self.pattern = kwargs["pattern"]
        if "default" in kwargs:
            self.default = kwargs["default"]

    @property
    def type(self) -> Literal["string"]:
        return "string"

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        MinMaxLength.dump(self, dest)
        CommonKeys.dump(self, dest)
        if self.enum:
            dest["enum"] = un_type(self.enum)
        if self.format:
            dest["format"] = self.format
        if self.pattern:
            dest["pattern"] = self.pattern
        if self.default:
            dest["default"] = self.default
        dest["type"] = self.type
        return dest

    @property
    def format(
        self,
    ) -> (
        Literal["date"]
        | Literal["date-time"]
        | Literal["password"]
        | Literal["byte"]
        | Literal["binary"]
        | str
        | None
    ):
        return self._format

    @format.setter
    def format(self, value: Any) -> None:
        if value in ["base64", "binary"]:
            raise SchemaMismatch(f"Trying to parse a FileType as StringType {value}")
        self._format = validate_key_type("format", [str, type(None)], {"format": value})

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, StringType):
            return False
        return (
            self.format == value.format
            and self.pattern == value.pattern
            and self.default == value.default
            and self.enum == value.enum
            and MinMaxLength.__eq__(self, value)
            and CommonKeys.__eq__(self, value)
        )


class ArrayType(CommonKeys):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        items: Any = kwargs.get("items")
        self.items = items
        if "uniqueItems" in kwargs:
            self.uniqueItems = kwargs["uniqueItems"]
        if "minItems" in kwargs:
            self.minItems = kwargs["minItems"]
        if "maxItems" in kwargs:
            self.maxItems = kwargs["maxItems"]
        if "default" in kwargs:
            self.default = kwargs["default"]

    _uniqueItems: Optional[bool] = None

    @property
    def uniqueItems(self) -> Optional[bool]:
        return self._uniqueItems

    @uniqueItems.setter
    def uniqueItems(self, value: Any) -> None:
        self._uniqueItems = is_value_type(value, [bool, type(None)])

    _minItems: Optional[int] = None

    @property
    def minItems(self) -> Optional[int]:
        return self._minItems

    @minItems.setter
    def minItems(self, value: Any) -> None:
        self._minItems = is_value_type(value, [int, type(None)])

    _maxItems: Optional[int] = None

    @property
    def maxItems(self) -> Optional[int]:
        return self._maxItems

    @maxItems.setter
    def maxItems(self, value: Any) -> None:
        self._maxItems = is_value_type(value, [int, type(None)])

    _default: Optional[str | list[Any]] = None

    @property
    def default(self) -> Optional[str | list[Any]]:
        return self._default

    @default.setter
    def default(self, value: Any) -> None:
        self._default = is_value_type(value, [list, type(None), str])

    _items: "TypeDeclaration"

    @property
    def items(self) -> "TypeDeclaration":
        return self._items

    @items.setter
    def items(self, value: Any) -> None:
        if value is None:
            raise SchemaMismatch("'items' must be present for an array")
        self._items = parse_type(value)

    @property
    def type(self) -> Literal["array"]:
        return "array"

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        super().dump(dest)
        dest["items"] = self.items.dump({})
        if self.uniqueItems is not None:
            dest["uniqueItems"] = self.uniqueItems
        if self.minItems:
            dest["minItems"] = self.minItems
        if self.maxItems:
            dest["maxItems"] = self.maxItems
        if self.default:
            dest["default"] = self.default
        dest["type"] = self.type
        return dest

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ArrayType):
            return False
        return (
            True
            if self.default == value.default
            and self.uniqueItems == value.uniqueItems
            and self.minItems == value.minItems
            and self.maxItems == value.maxItems
            and self.default == value.default
            and self.items == value.items
            else False
        )


class ObjectType(CommonKeys):
    _required: Optional[list[str]] = None

    @property
    def required(self) -> Optional[list[str]]:
        return self._required

    @required.setter
    def required(self, value: Any) -> None:
        self._required = validate_key_type_lambda(
            "required",
            [
                lambda x: isinstance(x, list)
                and all(isinstance(item, str) for item in x),
                lambda x: x is None,
            ],
            {"required": value},
        )

    _additionalProperties: Optional[bool] = None

    @property
    def additionalProperties(self) -> Optional[bool]:
        return self._additionalProperties

    @additionalProperties.setter
    def additionalProperties(self, value: Any) -> None:
        self._additionalProperties = is_value_type(value, [bool, type(None)])

    _minProperties: Optional[int] = None

    @property
    def minProperties(self) -> Optional[int]:
        return self._minProperties

    @minProperties.setter
    def minProperties(self, value: Any) -> None:
        self._minProperties = is_value_type(value, [int, type(None)])

    _maxProperties: Optional[int] = None

    @property
    def maxProperties(self) -> Optional[int]:
        return self._maxProperties

    @maxProperties.setter
    def maxProperties(self, value: Any) -> None:
        self._maxProperties = is_value_type(value, [int, type(None)])

    _default: Optional[JSON_DICT] = None

    @property
    def default(self) -> Optional[JSON_DICT]:
        return self._default

    @default.setter
    def default(self, value: Any) -> None:
        self._default = is_value_type(value, [dict, type(None)])

    _properties: Optional[dict[str, "TypeDeclaration"]] = None

    @property
    def properties(self) -> Optional[dict[str, "TypeDeclaration"]]:
        return self._properties

    @properties.setter
    def properties(self, value: Any) -> None:
        if type(value) is type(None):
            self._properties = None
            return
        if type(value) is not dict:
            raise SchemaMismatch(
                f"Object 'properties' must be a dictionary or None, is {type(value)}"
            )
        props: dict[str, "TypeDeclaration"] = {}
        for key in value:
            props[key] = parse_type(value[key])

        self._properties = props

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if "properties" in kwargs:
            self.properties = kwargs["properties"]
        if "required" in kwargs:
            self.required = kwargs["required"]
        if "additionalProperties" in kwargs:
            self.additionalProperties = validate_key_type(
                "additionalProperties", bool, kwargs
            )
        if "minProperties" in kwargs:
            self.minProperties = kwargs["minProperties"]
        if "maxProperties" in kwargs:
            self.maxProperties = kwargs["maxProperties"]
        if "default" in kwargs:
            self.default = kwargs["default"]

    @property
    def type(self) -> Literal["object"]:
        return "object"

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        super().dump(dest)
        if self.required is not None:
            dest["required"] = un_type(self.required)
        if self.additionalProperties is not None:
            dest["additionalProperties"] = self.additionalProperties
        if self.minProperties is not None:
            dest["minProperties"] = self.minProperties
        if self.maxProperties is not None:
            dest["maxProperties"] = self.maxProperties
        if self.default is not None:
            dest["default"] = self.default
        dest["type"] = self.type

        if self.properties:
            dest["properties"] = {
                key: self.properties[key].dump({}) for key in self.properties
            }
        return dest

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ObjectType):
            return False

        this_props = self.properties
        that_props = value.properties

        if this_props or that_props:
            if this_props is None or that_props is None:
                return False

            for key in this_props:
                if key not in that_props:
                    return False
                if this_props[key] != that_props[key]:
                    return False
            for key in that_props:
                if key not in this_props:
                    return False
                if this_props[key] != that_props[key]:
                    return False

        return (
            True
            if self.default == value.default
            and self.required == value.required
            and self.additionalProperties == value.additionalProperties
            and self.minProperties == value.minProperties
            and self.maxProperties == value.maxProperties
            and self.default == value.default
            else False
        )


ExplicitTypeDeclaration: TypeAlias = (
    BooleanType
    | FileType
    | IntegerType
    | NumberType
    | StringType
    | ArrayType
    | ObjectType
)


class OneOfType:
    _oneOf: list["TypeDeclaration"]

    def __init__(self, **kwargs: Any) -> None:
        if "oneOf" in kwargs:
            self.oneOf = kwargs["oneOf"]

    @property
    def oneOf(self) -> list["TypeDeclaration"]:
        return self._oneOf

    @oneOf.setter
    def oneOf(self, value: Any) -> None:
        self._oneOf = [
            parse_type(item)
            for item in validate_key_type("value", list, {"value": value})
        ]

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        dest["oneOf"] = [item.dump({}) for item in self.oneOf]
        return dest

    def append(self, component: "TypeDeclaration") -> None:
        self._oneOf = (self._oneOf or []) + [component]


class AnyOfType:
    _anyOf: list["TypeDeclaration"]

    def __init__(self, **kwargs: Any) -> None:
        if "anyOf" in kwargs:
            self.anyOf = kwargs["anyOf"]

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        dest["anyOf"] = [item.dump({}) for item in self.anyOf]
        return dest

    @property
    def anyOf(self) -> list["TypeDeclaration"]:
        return self._anyOf

    @anyOf.setter
    def anyOf(self, value: Any) -> None:
        self._anyOf = [
            parse_type(item)
            for item in validate_key_type("value", list, {"value": value})
        ]

    def append(self, component: "TypeDeclaration") -> None:
        self._anyOf = (self._anyOf or []) + [component]


class AllOfType:
    _allOf: list["TypeDeclaration"]

    def __init__(self, **kwargs: Any) -> None:
        if "allOf" in kwargs:
            self.allOf = kwargs["allOf"]

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        dest["allOf"] = [item.dump({}) for item in self.allOf]
        return dest

    @property
    def allOf(self) -> list["TypeDeclaration"]:
        return self._allOf

    @allOf.setter
    def allOf(self, value: Any) -> None:
        self._allOf = [
            parse_type(item)
            for item in validate_key_type("value", list, {"value": value})
        ]

    def append(self, component: "TypeDeclaration") -> None:
        self._allOf = (self._allOf or []) + [component]


class RefType:
    ref: str

    def __init__(self, **kwargs: Any) -> None:
        if "$ref" in kwargs:
            self.ref = kwargs["$ref"]

    def dump(self, dest: JSON_DICT) -> JSON_DICT:
        dest["$ref"] = self.ref
        return dest


def parse_type(value: JSON_DICT) -> "TypeDeclaration":
    if not isinstance(value, dict):
        raise SchemaMismatch(f"Couldn't decode type {value} <not an object?>")
    if "type" in value:
        match value["type"]:
            case "number":
                return NumberType(**value)
            case "integer":
                return IntegerType(**value)
            case "string":
                return switch_string_file(value)
            case "boolean":
                return BooleanType(**value)
        raise SchemaMismatch(f"Couldn't decode object type {value}")

    if "oneOf" in value:
        return OneOfType(**value)
    if "allOf" in value:
        return AllOfType(**value)
    if "anyOf" in value:
        return AnyOfType(**value)
    if "$ref" in value:
        return RefType(**value)
    raise SchemaMismatch(f"Schema can not be decoded {value}")


def switch_string_file(value: JSON_DICT) -> StringType | FileType:
    if "format" in value and value["format"] in ["base64", "binary"]:
        return FileType(**value)
    return StringType(**value)


TypeDeclaration: TypeAlias = (
    OneOfType | RefType | AllOfType | AnyOfType | ExplicitTypeDeclaration
)
