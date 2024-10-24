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

from code_generator._class.utils import (
    multi_dict_detector,
    optional_detector,
    simple_dict_detector,
    strip_optional,
    type_extractor,
)


def is_if_a_value_in_kwargs(fi: ast.If, target_id: str) -> bool:
    if isinstance(fi.test, ast.Compare):
        if isinstance(fi.test.left, ast.Constant):
            if fi.test.left.value == target_id:
                if isinstance(fi.test.comparators[0], ast.Name):
                    if fi.test.comparators[0].id == "kwargs":
                        return True
    return False


def else_raise_schema(target_id: str, typeof: str) -> list[ast.stmt]:
    return (
        ast.parse(
            f"if True:\n\tpass\nelse:\n\traise SchemaMismatch('Object must contain \"{target_id}\" value ({typeof})')"
        ).body[0]
    ).orelse  # type: ignore


def simple_template(target_id: str, typeof: str) -> ast.If:
    return ast.parse(
        f"if '{target_id}' in kwargs:\n\tself._{target_id} = validate_key_type('{target_id}', {typeof}, {'{'}'{target_id}': kwargs['{target_id}']{'}'})\n"
    )  # type:ignore


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


def is_dict(ass: ast.AnnAssign) -> bool:
    return (
        simple_dict_detector(ass) is not False or multi_dict_detector(ass) is not False
    )


def multi_try(target_id: str, right: str) -> ast.Try:
    return ast.parse(f"""try:
    {right.lower()}_entry = {right}(**kwargs['{target_id}'][{target_id.lower()}_key])
    self.{target_id}[{target_id.lower()}_key] = {right.lower()}_entry
    continue
except Exception as {right}_error:
    {target_id}_errors.append(f"__CLASS__ {target_id} instance failed on parsing {right}: {"{"}{right}_error{"}"}")
""").body[0]  # type: ignore


def multi_dict_for(target_id: str, rights: list[str]) -> ast.For:
    rof: ast.For = ast.parse(f"""for {target_id.lower()}_key in kwargs['{target_id}']:
    {target_id}_errors = []
    raise SchemaMismatch(f"__CLASS__ {target_id} parse failed on the following error list:{{chr(92)}} {"{"}f'{{chr(92)}}'.join({target_id}_errors){"}"}")
""").body[0]  # type: ignore
    for right in rights[::-1]:
        rof.body.insert(1, multi_try(target_id, right))
    return rof


def multi_dict_template(target_id: str, rights: list[str]):
    fi: ast.If = ast.parse(
        f"""if "{target_id}" in kwargs:\n\tself.{target_id} = {{}}"""
    ).body[0]  # type: ignore
    fi.body.append(multi_dict_for(target_id, rights))
    return fi


def simple_dict_template(target_id: str, right: str) -> ast.If:
    return ast.parse(f"""if "{target_id}" in kwargs:
    self.{target_id} = {"{}"}
    for {target_id}_key in kwargs['{target_id}']:
        try:
            self.{target_id}[{target_id}_key] = {right}(**kwargs['{target_id}'][{target_id}_key])
        except Exception as {target_id}_error:
            raise SchemaMismatch(f"__CLASS__ {target_id} instance must be of type {right},{"{"}{target_id}_error{":}"}")
""").body[0]  # type: ignore


def resolve_entry(
    fun: ast.FunctionDef,
    ass: ast.AnnAssign,
    target_id: str,
    is_optional: bool,
    typeof: str,
) -> None:
    for line in fun.body:
        if isinstance(line, ast.If) and is_if_a_value_in_kwargs(line, target_id):
            if not is_optional and len(line.orelse) == 0:
                line.orelse = else_raise_schema(target_id, typeof)
            return
    else:
        sd = simple_dict_detector(ass)
        md = multi_dict_detector(ass)
        if sd is not False:
            fi = simple_dict_template(target_id, sd[1])
        elif md is not False:
            fi = multi_dict_template(target_id, md[1])

        else:
            fi = simple_template(target_id, typeof)
        if is_optional is False:
            fi.orelse = else_raise_schema(target_id, typeof)
        fun.body.append(fi)
        return


def resolve__init__(ass: ast.AnnAssign, target_id: str, body: list[ast.stmt]) -> None:
    is_optional = optional_detector(ass)
    _ass: ast.AnnAssign = ast.parse(f"var:{ast.unparse(strip_optional(ass))}").body[0]  # type: ignore

    for line in body:
        if isinstance(line, ast.FunctionDef) and line.name == "__init__":
            resolve_entry(line, _ass, target_id, is_optional, type_extractor(ass))
            return
    else:
        fun: ast.FunctionDef = ast.parse(
            "def __init__(self,**kwargs:Any)->None:\n\tself.source=kwargs"
        ).body[0]  # type: ignore
        add_to__init__(fun, target_id, is_optional, type_extractor(ass))
        body.append(fun)
