from typing import Any
from ..tools import merge_dict


COMMON_KEYS_GOOD_DATASET_A = {"nullable": True, "title": "Test title"}
COMMON_KEYS_GOOD_DATASET_B = {"nullable": True, "title": "Test title B"}
COMMON_KEYS_GOOD_DATASET_C = {"nullable": False, "title": "Test title B"}
COMMON_KEYS_BAD_DATASET_A = {"nullable": "can't be string", "title": False}
MIN_MAX_INT_GOOD_DATASET_A = {"maxLength": 2, "minLength": 1}
MIN_MAX_INT_GOOD_DATASET_B = {"maxLength": 200, "minLength": 100}
MIN_MAX_INT_BAD_DATASET_A = {"maxLength": 123, "minLength": "123"}
MIN_MAX_INT_BAD_DATASET_B = {"maxLength": "123", "minLength": 123}
MIN_MAX_FLOAT_GOOD_DATASET_A = {"maxLength": 2.200, "minLength": 1.100}
MIN_MAX_FLOAT_GOOD_DATASET_B = {"maxLength": 200.200, "minLength": 100.100}
MIN_MAX_FLOAT_BAD_DATASET_A = {"maxLength": 123, "minLength": "123"}
MIN_MAX_FLOAT_BAD_DATASET_B = {"maxLength": "123", "minLength": 123}
NUMBER_RULES_FLOAT_GOOD_DATASET_A = {
    "exclusiveMinimum": False,
    "exclusiveMaximum": False,
    "maximum": 1.1,
    "minimum": 2.1,
    "multipleOf": float(2.0),
}
NUMBER_RULES_FLOAT_GOOD_DATASET_B = {
    "exclusiveMinimum": True,
    "exclusiveMaximum": True,
    "maximum": 11.1,
    "minimum": 22.1,
    "multipleOf": 32.0,
}
NUMBER_RULES_FLOAT_BAD_DATASET_A = {
    "exclusiveMinimum": "True",
    "exclusiveMaximum": True,
    "maximum": 121.1,
    "minimum": 212.1,
    "multipleOf": 32.0,
}
NUMBER_RULES_INT_GOOD_DATASET_A = {
    "exclusiveMinimum": False,
    "exclusiveMaximum": False,
    "maximum": 1,
    "minimum": 2,
    "multipleOf": 2,
}
NUMBER_RULES_INT_GOOD_DATASET_B = {
    "exclusiveMinimum": True,
    "exclusiveMaximum": True,
    "maximum": 12,
    "minimum": 21,
    "multipleOf": 23,
}
NUMBER_RULES_INT_BAD_DATASET_A = {
    "exclusiveMinimum": "True",
    "exclusiveMaximum": True,
    "maximum": 121,
    "minimum": 212,
    "multipleOf": 32,
}
BOOLEAN_DIFF_A = {"default": False}
BOOLEAN_DIFF_B = {"default": True}
BOOLEAN_DIFF_BAD_A = {"default": 2}
BOOLEAN_DIFF_BAD_B = {"default": "False"}
BOOLEAN_DIFF_BAD_C = {"default": ["False"]}
STRING_DIFF_A = {
    "enum": ["asd", "dasd"],
    "format": "email",
    "pattern": "/re/",
}
STRING_DIFF_B: dict[str, Any] = {}
STRING_DIFF_BAD_A = {
    "default": True,
    "format": "email",
    "pattern": "/re/",
}
STRING_DIFF_BAD_B = {"default": 2}
STRING_DIFF_BAD_C = {"default": "False"}
BOOLEAN_GOOD_DATASET_A = merge_dict(BOOLEAN_DIFF_A, COMMON_KEYS_GOOD_DATASET_A)
BOOLEAN_GOOD_DATASET_B = merge_dict(BOOLEAN_DIFF_B, COMMON_KEYS_GOOD_DATASET_A)
BOOLEAN_BAD_DATASET_A = merge_dict(BOOLEAN_DIFF_BAD_A, COMMON_KEYS_GOOD_DATASET_A)
STRING_GOOD_DATASET_A = merge_dict(
    MIN_MAX_INT_GOOD_DATASET_A,
    COMMON_KEYS_GOOD_DATASET_A,
    STRING_DIFF_A,
)
STRING_GOOD_DATASET_B = merge_dict(
    MIN_MAX_INT_GOOD_DATASET_A,
    COMMON_KEYS_GOOD_DATASET_A,
    STRING_DIFF_B,
)
STRING_BAD_DATASET_A = merge_dict(
    MIN_MAX_INT_GOOD_DATASET_A,
    COMMON_KEYS_GOOD_DATASET_A,
    STRING_DIFF_BAD_A,
)
FILE_GOOD_DIFF_A = {"format": "base64", "type": "string"}
FILE_GOOD_DATASET_A = merge_dict(COMMON_KEYS_GOOD_DATASET_A, FILE_GOOD_DIFF_A)
FILE_GOOD_DIFF_B = {"format": "binary", "type": "string"}
FILE_GOOD_DATASET_B = merge_dict(COMMON_KEYS_GOOD_DATASET_B, FILE_GOOD_DIFF_B)
FILE_BAD_DIFF_A = {"format": "stuff"}
FILE_BAD_DATASET_C = merge_dict(COMMON_KEYS_GOOD_DATASET_B, FILE_BAD_DIFF_A)
NUMBER_GOOD_DIFF_A = {"format": "float", "type": "number"}
NUMBER_GOOD_DIFF_B = {"format": "double", "type": "number"}
NUMBER_GOOD_DIFF_C = {"type": "number"}
INTEGER_GOOD_DIFF_A = {"format": "int32", "type": "integer"}
INTEGER_GOOD_DIFF_B = {"format": "int64", "type": "integer"}
INTEGER_GOOD_DIFF_C = {"type": "integer"}
NUMBER_BAD_DIFF_A = {"format": "number"}
NUMBER_GOOD_DATASET_A = merge_dict(
    NUMBER_GOOD_DIFF_A,
    MIN_MAX_FLOAT_GOOD_DATASET_A,
    NUMBER_RULES_FLOAT_GOOD_DATASET_A,
    COMMON_KEYS_GOOD_DATASET_A,
)
NUMBER_GOOD_DATASET_B = merge_dict(
    NUMBER_GOOD_DIFF_A,
    MIN_MAX_INT_GOOD_DATASET_A,
    NUMBER_RULES_FLOAT_GOOD_DATASET_A,
    COMMON_KEYS_GOOD_DATASET_A,
)
NUMBER_GOOD_DATASET_C = merge_dict(
    NUMBER_GOOD_DIFF_A,
    MIN_MAX_INT_GOOD_DATASET_A,
    NUMBER_RULES_INT_GOOD_DATASET_A,
    COMMON_KEYS_GOOD_DATASET_A,
)
NUMBER_GOOD_DATASET_D = merge_dict(
    NUMBER_GOOD_DIFF_A,
    MIN_MAX_FLOAT_GOOD_DATASET_A,
    NUMBER_RULES_INT_GOOD_DATASET_A,
    COMMON_KEYS_GOOD_DATASET_A,
)
NUMBER_GOOD_DATASET_E = merge_dict(
    NUMBER_GOOD_DIFF_B,
    MIN_MAX_FLOAT_GOOD_DATASET_B,
    NUMBER_RULES_FLOAT_GOOD_DATASET_B,
    COMMON_KEYS_GOOD_DATASET_B,
)
NUMBER_GOOD_DATASET_F = merge_dict(
    NUMBER_GOOD_DIFF_B,
    MIN_MAX_INT_GOOD_DATASET_B,
    NUMBER_RULES_FLOAT_GOOD_DATASET_B,
    COMMON_KEYS_GOOD_DATASET_B,
)
NUMBER_GOOD_DATASET_G = merge_dict(
    NUMBER_GOOD_DIFF_B,
    MIN_MAX_INT_GOOD_DATASET_B,
    NUMBER_RULES_INT_GOOD_DATASET_B,
    COMMON_KEYS_GOOD_DATASET_B,
)
NUMBER_GOOD_DATASET_H = merge_dict(
    NUMBER_GOOD_DIFF_B,
    MIN_MAX_FLOAT_GOOD_DATASET_B,
    NUMBER_RULES_INT_GOOD_DATASET_B,
    COMMON_KEYS_GOOD_DATASET_B,
)

NUMBER_BAD_DATASET_A = merge_dict(
    NUMBER_BAD_DIFF_A,
    MIN_MAX_FLOAT_GOOD_DATASET_A,
    NUMBER_RULES_FLOAT_GOOD_DATASET_A,
    COMMON_KEYS_GOOD_DATASET_A,
)

ARRAY_GOOD_DIFF_A = {
    "type": "array",
    "uniqueItems": False,
    "minItems": 5,
    "maxItems": 6,
    "default": [],
}
ARRAY_GOOD_DIFF_B = {
    "type": "array",
    "uniqueItems": True,
}
ARRAY_GOOD_DIFF_C = {"type": "array", "maxItems": 6}
