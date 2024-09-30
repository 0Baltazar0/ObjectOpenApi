from typing import Any, Callable

from .parse_errors import SchemaMismatch


def is_value_type(value: Any, types: Any | list[Any]) -> Any:
    if isinstance(types, list):
        if not any([type(value) is kt for kt in types]):
            raise SchemaMismatch(f"Expecting one of {types}, getting {type(value)}!")
    elif not isinstance(value, types):
        raise SchemaMismatch(f"Expecting {types}, getting {type(value)}!")
    return value


def validate_key_type(
    key_name: str, key_type: Any | list[Any], data: dict[str, Any]
) -> Any:
    if isinstance(key_type, list):
        if not any([type(data[key_name]) is kt for kt in key_type]):
            raise SchemaMismatch(
                f"Expecting one of {key_type}, getting {type(data[key_name])} on key-word {key_name}!"
            )
    elif type(data[key_name]) is not key_type:
        raise SchemaMismatch(
            f"Expecting {key_type}, getting {type(data[key_name])} on key-word {key_name}!"
        )
    return data[key_name]


def validate_key_type_lambda(
    key_name: str,
    key_type: Callable[[Any], bool] | list[Callable[[Any], bool]],
    data: dict[str, Any],
) -> Any:
    if isinstance(key_type, list):
        if not any([kt(data[key_name]) for kt in key_type]):
            raise SchemaMismatch(
                f"No lambda function was able to validate value, getting {type(data[key_name])} on key-word {key_name}!"
            )
    elif key_type(data[key_name]) is False:
        raise SchemaMismatch(
            f"Lambda function failed on parsing the value, getting {type(data[key_name])} on key-word {key_name}!"
        )
    return data[key_name]


def validate_key_exact(
    key_name: str,
    key_type: Any | list[Any],
    data: dict[str, Any],
) -> Any:
    if isinstance(key_type, list):
        if not any([kt == data[key_name] for kt in key_type]):
            raise SchemaMismatch(
                f"Expecting one of {key_type}, getting {type(data[key_name])} on key-word {key_name}!"
            )
    elif key_type != data[key_name]:
        raise SchemaMismatch(
            f"Expecting {key_type}, getting {type(data[key_name])} on key-word {key_name}!"
        )
    return data[key_name]
