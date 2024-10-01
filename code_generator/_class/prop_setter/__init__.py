import ast


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
                f"@{target_id}.setter\ndef {target_id}(self,value:{ast.unparse(ass.annotation)})->None:\n\tself._{target_id} = value"
            ).body[0]
            body.insert(body.index(ass) + 1, has_setter)
