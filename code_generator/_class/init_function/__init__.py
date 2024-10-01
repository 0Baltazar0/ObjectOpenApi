import ast

from code_generator._class.utils import optional_detector, type_extractor


def is_if_a_value_in_kwargs(fi: ast.If, target_id: str) -> bool:
    if isinstance(fi.test, ast.Compare):
        if isinstance(fi.test.left, ast.Constant):
            if fi.test.left.value == target_id:
                if isinstance(fi.test.comparators[0], ast.Name):
                    if fi.test.comparators[0].id == "kwargs":
                        return True
    return False


def add_to__init__(
    fun: ast.FunctionDef, target_id: str, is_optional: bool, typeof: str
) -> None:
    for line in fun.body:
        if (
            is_optional
            and isinstance(line, ast.If)
            and is_if_a_value_in_kwargs(line, target_id)
        ):
            if not is_optional and len(line.orelse) == 0:
                fi = ast.parse(
                    f"if '{target_id}' in kwargs:\n\tself._{target_id} = validate_key_type('{target_id}', {typeof}, {'{'}'{target_id}': kwargs['{target_id}']{'}'})\nelse:\n\traise SchemaMismatch('Object must contain \"{target_id}\" value ({typeof})')"
                ).body[0]
                line.orelse = fi.orelse

            return
    else:
        if is_optional:
            fi = ast.parse(
                f"if '{target_id}' in kwargs:\n\tself._{target_id} = validate_key_type('{target_id}', {typeof}, {'{'}'{target_id}': kwargs['{target_id}']{'}'})"
            ).body[0]
            fun.body.append(fi)
        else:
            fi = ast.parse(
                f"if '{target_id}' in kwargs:\n\tself._{target_id} = validate_key_type('{target_id}', {typeof}, {'{'}'{target_id}': kwargs['{target_id}']{'}'})\nelse:\n\traise SchemaMismatch('Object must contain \"{target_id}\" value ({typeof})')"
            ).body[0]
            fun.body.append(fi)


def resolve__init__(ass: ast.AnnAssign, target_id: str, body: list[ast.stmt]) -> None:
    is_optional = optional_detector(ass)

    for line in body:
        if isinstance(line, ast.FunctionDef) and line.name == "__init__":
            add_to__init__(line, target_id, is_optional, type_extractor(ass))
            return
    else:
        fun: ast.FunctionDef = ast.parse(
            "def __init__(self,**kwargs:Any)->None:\n\tself.source=kwargs"
        ).body[0]  # type: ignore
        add_to__init__(fun, target_id, is_optional, type_extractor(ass))
        body.append(fun)
