import typing


JSON_LIST: typing.TypeAlias = list["JSON_TYPE"]
JSON_DICT: typing.TypeAlias = dict[str, "JSON_TYPE"]
JSON_TYPE: typing.TypeAlias = (
    dict[str, "JSON_TYPE"] | list["JSON_TYPE"] | str | int | float | bool | None
)
