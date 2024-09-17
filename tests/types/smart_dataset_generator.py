from copy import deepcopy
from typing import Any
import os
from tests.tools import merge_dict

optimisation = int(os.environ.get("LONG_DATASET_SKIP", 2))
optimisation_offset = int(os.environ.get("OFFSET_DATASET", 0))
variety = min(int(os.environ.get("MAX_VARIETY", 3)), 10)
variety_offset = min(int(os.environ.get("OFFSET_VARIETY", 0)), 9)

STRING_VARIANTS = [
    "TestString123",
    "HelloWorld_2024",
    "Sample_Text@#",
    "AlphaBetaGamma,12,3",
    "QuickBrownFox_,Ju,mp,s",
    "LoremIpsumDolo,rSit,",
    "Python_Testing_One,",
    "EdgeCase_$$$_Check",
    "RandomString09876",
    "UnitTest_Example123!",
][variety_offset : variety_offset + variety]
INT_VARIANTS = [63, 14, 90, 21, 69, 74, 100, 5, 15, 62][
    variety_offset : variety_offset + variety
]
FLOAT_VARIANTS = [78.58, 29.16, 14.60, 92.74, 80.62, 2.78, 59.95, 62.49, 17.20, 59.69][
    variety_offset : variety_offset + variety
]
BOOL_VARIANTS = [True, False]


def all_but(except_var: Any):
    ret = []
    for var in [STRING_VARIANTS, INT_VARIANTS, FLOAT_VARIANTS, BOOL_VARIANTS]:
        if var == except_var:
            continue
        ret += var
    return ret[optimisation_offset::optimisation]


def simple_types_but(except_var: Any) -> list[dict[str, Any]]:
    ret = []
    for var in [
        generate_int,
        generate_boolean,
        generate_number,
        generate_string,
        generate_file,
    ]:
        if var == except_var:
            continue
        ret += var()
    return ret


def recursive_combinations(options: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    if len(options) == 0:
        return []

    if len(options) == 1:
        return deepcopy(options[0])
    rest = deepcopy(options)
    selected = rest.pop(0)
    propogate = recursive_combinations(rest)
    result: list[dict[str, Any]] = [{}]
    for item in selected:
        for ret in propogate:
            result.append(merge_dict(deepcopy(ret), deepcopy(item)))
    return result


def combine_options(
    required: list[dict[str, Any]], optionals: list[list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    res: list[dict[str, Any]] = []
    rec_combinations = recursive_combinations(optionals)
    for r in required:
        if len(r.keys()) > 0:
            res.append(deepcopy(r))
        for c in rec_combinations[1:]:
            res.append(merge_dict(deepcopy(r), deepcopy(c)))
    return res


def generate_common_keys() -> list[dict[str, Any]]:
    required_keys = [{}]
    optional_keys = [
        [{"nullable": x} for x in BOOL_VARIANTS],
        [{"title": x} for x in STRING_VARIANTS],
    ]
    return combine_options(required_keys, optional_keys)


def generate_bad_common_keys() -> list[dict[str, Any]]:
    required_keys = [{}]
    optional_keys = [
        [{"nullable": x} for x in all_but(BOOL_VARIANTS)],
        [{"title": x} for x in all_but(STRING_VARIANTS)],
    ]
    return combine_options(required_keys, optional_keys)[1:]


def generate_good_min_max() -> list[dict[str, Any]]:
    required_keys = [{}]
    optional_keys = [
        [{"maxLength": x} for x in INT_VARIANTS],
        [{"minLength": x} for x in INT_VARIANTS],
    ]
    return combine_options(required_keys, optional_keys)


def generate_bad_min_max() -> list[dict[str, Any]]:
    required_keys = [{}]
    optional_keys = [
        [{"maxLength": x} for x in all_but(INT_VARIANTS)],
        [{"minLength": x} for x in all_but(INT_VARIANTS)],
    ]
    return combine_options(required_keys, optional_keys)


def generate_good_number_rules_int() -> list[dict[str, Any]]:
    required_keys = [{}]
    optional_keys = [
        [{"exclusiveMinimum": x} for x in BOOL_VARIANTS],
        [{"exclusiveMaximum": x} for x in BOOL_VARIANTS],
        [{"maximum": x} for x in INT_VARIANTS],
        [{"minimum": x} for x in INT_VARIANTS],
        [{"multipleOf": x} for x in INT_VARIANTS],
    ]
    return combine_options(required_keys, optional_keys)


def generate_bad_number_rules_int() -> list[dict[str, Any]]:
    required_keys = [{}]
    optional_keys = [
        [{"exclusiveMinimum": x} for x in all_but(BOOL_VARIANTS)],
        [{"exclusiveMaximum": x} for x in all_but(BOOL_VARIANTS)],
        [{"maximum": x} for x in all_but(INT_VARIANTS)],
        [{"minimum": x} for x in all_but(INT_VARIANTS)],
        [{"multipleOf": x} for x in all_but(INT_VARIANTS)],
    ]
    return combine_options(required_keys, optional_keys)[1:]


def generate_good_number_rules_float() -> list[dict[str, Any]]:
    required_keys = [{}]
    optional_keys = [
        [{"exclusiveMinimum": x} for x in BOOL_VARIANTS],
        [{"exclusiveMaximum": x} for x in BOOL_VARIANTS],
        [{"maximum": x} for x in FLOAT_VARIANTS],
        [{"minimum": x} for x in FLOAT_VARIANTS],
        [{"multipleOf": x} for x in FLOAT_VARIANTS],
    ]
    return combine_options(required_keys, optional_keys)


def generate_bad_number_rules_float() -> list[dict[str, Any]]:
    required_keys = [{}]
    optional_keys = [
        [{"exclusiveMinimum": x} for x in all_but(BOOL_VARIANTS)],
        [{"exclusiveMaximum": x} for x in all_but(BOOL_VARIANTS)],
        [{"maximum": x} for x in all_but(FLOAT_VARIANTS)],
        [{"minimum": x} for x in all_but(FLOAT_VARIANTS)],
        [{"multipleOf": x} for x in all_but(FLOAT_VARIANTS)],
    ]
    return combine_options(required_keys, optional_keys)


def generate_boolean() -> list[dict[str, Any]]:
    required_keys = [
        {"type": "boolean"},
    ]
    optional_keys = [
        [{"default": BOOL_VARIANTS[x]} for x in range(len(BOOL_VARIANTS))],
        generate_common_keys()[1:],
    ]
    return combine_options(required_keys, optional_keys)


def generate_boolean_bad() -> list[dict[str, Any]]:
    required_keys = [
        {"type": "boolean"},
    ]
    optional_keys = [
        [{"default": x} for x in all_but(BOOL_VARIANTS)],
        generate_bad_common_keys()[1:],
    ]
    return combine_options(required_keys, optional_keys)[1:]


def generate_string() -> list[dict[str, Any]]:
    required_keys = [{"type": "string"}]
    optional_keys = [
        [{"enum": x for x in STRING_VARIANTS}],
        [{"format": "email"}],
        [{"pattern": f"/{x}/" for x in STRING_VARIANTS}],
        generate_common_keys()[1:],
        generate_good_min_max()[1:],
    ]
    return combine_options(required_keys, optional_keys)


def generate_string_bad() -> list[dict[str, Any]]:
    required_keys = [{"type": "string"}]
    optional_keys = [
        [{"enum": x for x in all_but(STRING_VARIANTS)}],
        [{"format": "email"}],
        [{"pattern": f"/{x}/" for x in all_but(STRING_VARIANTS)}],
        generate_bad_common_keys()[optimisation_offset::optimisation],
        generate_bad_min_max()[optimisation_offset::optimisation],
    ]
    return combine_options(required_keys, optional_keys)[1:]


def generate_int() -> list[dict[str, Any]]:
    required_keys = [{"type": "integer"}]
    optional_keys = [
        [{"format": "int32"}, {"format": "int64"}],
        generate_common_keys()[1:],
        generate_good_number_rules_int()[1:],
    ]
    return combine_options(required_keys, optional_keys)


def generate_int_bad() -> list[dict[str, Any]]:
    required_keys = [{"type": "integer"}]
    optional_keys = [
        [{"format": x} for x in all_but(None)],
        generate_bad_common_keys(),
        generate_bad_number_rules_int(),
    ]
    return combine_options(required_keys, optional_keys)[1:]


def generate_number() -> list[dict[str, Any]]:
    required_keys = [{"type": "number"}]
    optional_keys = [
        [{"format": "float"}, {"format": "double"}],
        generate_common_keys(),
        generate_good_number_rules_float(),
    ]
    return combine_options(required_keys, optional_keys)


def generate_number_bad() -> list[dict[str, Any]]:
    required_keys = [{"type": "number"}]
    optional_keys = [
        [{"format": all_but(None)}, {"format": all_but(None)}],
        generate_bad_common_keys(),
        generate_bad_number_rules_float(),
    ]
    return combine_options(required_keys, optional_keys)[1:]


def generate_file() -> list[dict[str, Any]]:
    required_keys = [{"type": "string", "format": x} for x in ["base64", "binary"]]
    optional_keys = [
        generate_common_keys(),
    ]
    return combine_options(required_keys, optional_keys)


def generate_file_bad() -> list[dict[str, Any]]:
    required_keys = [{"type": "string"}]
    optional_keys = [
        [{"format": x} for x in all_but(None)],
        generate_bad_common_keys(),
    ]
    return combine_options(required_keys, optional_keys)[1:]


def generate_array() -> list[dict[str, Any]]:
    simple_types = simple_types_but(None)
    required_keys = [{"type": "array", "items": x} for x in simple_types]
    optional_keys = [
        [{"uniqueItems": x} for x in BOOL_VARIANTS],
        [{"minItems": x} for x in INT_VARIANTS],
        [{"maxItems": x} for x in INT_VARIANTS],
    ]
    return combine_options(required_keys, optional_keys)


def generate_array_bad() -> list[dict[str, Any]]:
    required_keys = [{"type": "array"}]
    optional_keys = [
        [{"items": x} for x in all_but(None)],
        [{"uniqueItems": x} for x in all_but(BOOL_VARIANTS)],
        [{"minItems": x} for x in all_but(INT_VARIANTS)],
        [{"maxItems": x} for x in all_but(INT_VARIANTS)],
    ]
    return combine_options(required_keys, optional_keys)


def generate_object() -> list[dict[str, Any]]:
    simple_types = simple_types_but(None)
    key_values = list(zip(STRING_VARIANTS, simple_types))
    kvs = {}
    for kv in key_values:
        kvs[kv[0]] = kv[1]
    required_keys = [{"type": "object", "properties": kvs}]
    optional_keys = [
        [{"additionalProperties": x} for x in BOOL_VARIANTS],
        [{"minProperties": x} for x in INT_VARIANTS],
        [{"maxProperties": x} for x in INT_VARIANTS],
    ]
    return combine_options(
        required_keys, optional_keys + [[{"required": [x[0] for x in key_values]}]]
    ) + combine_options([{"type": "object"}], optional_keys)


def generate_object_bad() -> list[dict[str, Any]]:
    key_values = list(zip(all_but(None), STRING_VARIANTS))
    kvs = {}
    for kv in key_values:
        kvs[kv[0]] = kv[1]
    required_keys = [{"type": "object", "properties": kvs}]
    optional_keys = [
        [{"additionalProperties": x} for x in all_but(BOOL_VARIANTS)],
        [{"minProperties": x} for x in all_but(INT_VARIANTS)],
        [{"maxProperties": x} for x in all_but(INT_VARIANTS)],
    ]
    return (
        combine_options(
            required_keys, optional_keys + [[{"required": [x[0] for x in key_values]}]]
        )[1:]
        + combine_options([{"type": "object"}], optional_keys)[1:]
    )


def generate_one_of() -> list[dict[str, Any]]:
    simple_types = simple_types_but(None)
    assert len(simple_types) != 0, "Simple types can not be an empty list"
    return [{"oneOf": simple_types[x:]} for x in range(len(simple_types))]


def generate_one_of_bad() -> list[dict[str, Any]]:
    return [{"oneOf": x} for x in all_but(None)]


def generate_any_of() -> list[dict[str, Any]]:
    simple_types = simple_types_but(None)
    assert len(simple_types) != 0, "Simple types can not be an empty list"
    return [{"anyOf": simple_types[x:]} for x in range(len(simple_types))]


def generate_any_of_bad() -> list[dict[str, Any]]:
    return [{"anyOf": x} for x in all_but(None)]


def generate_all_of() -> list[dict[str, Any]]:
    simple_types = simple_types_but(None)
    assert len(simple_types) != 0, "Simple types can not be an empty list"
    return [{"allOf": simple_types[x:]} for x in range(len(simple_types))]


def generate_all_of_bad() -> list[dict[str, Any]]:
    return [{"allOf": x} for x in all_but(None)]


if __name__ == "__main__":
    import json

    all_simple_types = [json.dumps(k, sort_keys=True) for k in simple_types_but(None)]
    keys = set(all_simple_types)
    collection_health = []
    for key in keys:
        count = all_simple_types.count(key)
        collection_health.append({"key": key, "occurence": count})
    with open("generated_data_health.json", "w") as out:
        import json

        json.dump(collection_health, out)
