"""
"title" in kwargs
<ast.If object at 0x0000026B97161BA0>
body
item:0
        <ast.Return object at 0x0000026B97162B00>
        value:<ast.Constant object at 0x0000026B96FA3010>
                <ast.Constant object at 0x0000026B96FA3010>
                kind:None
                        None
                n:False
                        False
                        denominator:1
                        imag:0
                        numerator:0
                        real:0
                s:False
                        False
                        denominator:1
                        imag:0
                        numerator:0
                        real:0
                value:False
                        False
                        denominator:1
                        imag:0
                        numerator:0
                        real:0
orelse
test:<ast.Compare object at 0x0000026B97160F40>
        <ast.Compare object at 0x0000026B97160F40>
        comparators
        item:0
                <ast.Name object at 0x0000026B97162920>
                ctx:<ast.Load object at 0x0000026B92EB9360>
                        <ast.Load object at 0x0000026B92EB9360>
                id:kwargs
                        kwargs
        left:<ast.Constant object at 0x0000026B97162230>
                <ast.Constant object at 0x0000026B97162230>
                kind:None
                        None
                n:title
                        title
                s:title
                        title
                value:title
                        title
        ops
        item:0
                <ast.In object at 0x0000026B92EBBEB0>
"""

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
        if isinstance(line, ast.If) and is_if_a_value_in_kwargs(line, target_id):
            if not is_optional and len(line.orelse) == 0:
                fi = ast.parse(
                    f"if '{target_id}' in kwargs:\n\tself._{target_id} = validate_key_type('{target_id}', {typeof}, {'{'}'{target_id}': kwargs['{target_id}']{'}'})\nelse:\n\traise SchemaMismatch('Object must contain \"{target_id}\" value ({typeof})')"
                ).body[0]
                line.orelse = fi.orelse  # type: ignore

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
