import ast


def optional_detector(ass: ast.AnnAssign) -> bool:
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
        return ast.unparse(ass.annotation.slice).replace("'", '"')
    return ast.unparse(ass.annotation).replace("'", '"')
