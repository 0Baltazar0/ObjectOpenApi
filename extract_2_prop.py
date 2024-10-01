import ast
import types


def pr(obj: object, indent=0) -> None:
    if isinstance(obj, types.BuiltinFunctionType):
        return
    if indent > 3:
        return
    indentation = "\t" * indent
    print(f"{indentation}{obj}")
    for item in dir(obj):
        if isinstance(getattr(obj, item), types.BuiltinFunctionType):
            continue
        if item.startswith("_") or item == "parent" or "line" in item or "col" in item:
            continue
        if isinstance(getattr(obj, item), list):
            print(f"{indentation}{item:}")
            for index in range(len(getattr(obj, item))):
                print(f"{indentation}item:{index}")
                pr(getattr(obj, item)[index], indent + 1)
        elif isinstance(getattr(obj, item), object):
            print(f"{indentation}{item}:{getattr(obj,item)}")
            pr(getattr(obj, item), indent + 1)
        else:
            print(f"{indentation}{item}:{getattr(obj,item)}")


def optional_detector(ass: ast.AnnAssign):
    return isinstance(ass.annotation, ast.Subscript) and (
        (
            isinstance(ass.annotation.value, ast.Name)
            and ass.annotation.value.id == "Optional"
        )
        or (
            isinstance(ass.annotation.value, ast.Attribute)
            and isinstance(ass.annotation.value.value, ast.Name)
            and ass.annotation.value.attr == "Optional"
            and ass.annotation.value.value.id == "typing"
        )
    )


def type_extractor(ass: ast.AnnAssign) -> str:
    if isinstance(ass.annotation, ast.Subscript):
        return ast.unparse(ass.annotation.slice)
    return ast.unparse(ass.annotation)


def property_detector(fun: ast.FunctionDef) -> bool:
    for decorator in fun.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id == "property":
            return True
    return False


def setter_detector(fun: ast.FunctionDef, prop_name: str) -> bool:
    for decorator in fun.decorator_list:
        if (
            isinstance(decorator, ast.Attribute)
            and decorator.attr == "setter"
            and isinstance(decorator.value, ast.Name)
            and decorator.value.id == prop_name
        ):
            return True
    return False


def resolve_property_set_get(
    ass: ast.AnnAssign, target_id: str, body: list[ast.stmt]
) -> None:
    has_getter = None
    has_setter = None
    for line in body:
        if isinstance(line, ast.FunctionDef):
            if line.name == target_id:
                if property_detector(line):
                    has_getter = line
                    continue
            if setter_detector(line, target_id):
                has_setter = line
                continue
        if has_getter and has_setter:
            return

    else:
        if not has_getter:
            has_getter = ast.parse(
                f"@property\ndef {target_id}(self)->{ast.unparse(ass.annotation)}:\n\treturn self._{target_id}"
            ).body[0]
            body.insert(body.index(ass) + 1, has_getter)
        if not has_setter:
            has_setter = ast.parse(
                f"@{target_id}.setter\ndef {target_id}(self,value:{ast.unparse(ass.annotation)})->None:\n\treturn self._{target_id} = value"
            ).body[0]


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


def is_dump_target(fi: ast.If, target_id: str) -> bool:
    """
    test:<ast.Compare object at 0x0000026B9708F070>
            <ast.Constant object at 0x0000026B9708FDF0>
                    kind:None
                    n:None
                    s:None
                    value:None
            left:<ast.Attribute object at 0x0000026B9708EAA0>
                    attr:var
                    ctx:<ast.Load object at 0x0000026B92EB9360>
                    s:None
                    value:None
            left:<ast.Attribute object at 0x0000026B9708EAA0>
                    attr:var
                    ctx:<ast.Load object at 0x0000026B92EB9360>
                    value:<ast.Name object at 0x0000026B9708C040>
                    attr:var
                    ctx:<ast.Load object at 0x0000026B92EB9360>
                    value:<ast.Name object at 0x0000026B9708C040>
                    value:<ast.Name object at 0x0000026B9708C040>
                            ctx:<ast.Load object at 0x0000026B92EB9360>
                            id:self
            <ast.IsNot object at 0x0000026B92EBBE50>
    """
    if (
        isinstance(fi.test, ast.Compare)
        and isinstance(fi.test.left, ast.Attribute)
        and isinstance(fi.test.left.value, ast.Name)
        and fi.test.left.value.id == "self"
    ):
        if fi.test.left.attr == target_id:
            return True
    return False


def add_to_dump(
    fn: ast.FunctionDef, target_id: str, is_optional: bool, types: str
) -> None:
    for line in fn.body:
        if is_optional:
            if isinstance(line, ast.If) and is_dump_target(line, target_id):
                pass


def resolve_dump(ass: ast.AnnAssign, target_id: str, body: list[ast.stmt]) -> None:
    is_optional = optional_detector(ass)

    for line in body:
        if isinstance(line, ast.FunctionDef) and line.name == "dump":
            add_to__init__(line, target_id, is_optional, type_extractor(ass))


def resolve__eq__(ass: ast.AnnAssign, target_id: str, body: list[ast.stmt]) -> None:
    is_optional = optional_detector(ass)

    for line in body:
        if isinstance(line, ast.FunctionDef) and line.name == "__eq__":
            add_to__init__(line, target_id, is_optional, type_extractor(ass))


def resolve_class(obj: ast.ClassDef):
    for line in obj.body:
        if isinstance(line, ast.AnnAssign) and isinstance(line.target, ast.Name):
            if line.target.id.startswith("_"):
                resolve_property_set_get(line, line.target.id[1:], obj.body)
                resolve__init__(line, line.target.id[1:], obj.body)
