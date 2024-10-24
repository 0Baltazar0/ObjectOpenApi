import ast
from typing import Literal


def strip_optional(ass: ast.AnnAssign) -> ast.expr:
    if isinstance(ass.annotation, ast.Subscript):
        if optional_detector(ass):
            return ass.annotation.slice
    return ass.annotation


def simple_dict_detector(ass: ast.AnnAssign) -> tuple[str, str] | Literal[False]:
    raw_ann = strip_optional(ass)
    if isinstance(raw_ann, ast.Subscript):
        if isinstance(raw_ann.value, ast.Name) and raw_ann.value.id == "dict":
            if isinstance(raw_ann.slice, ast.Tuple):
                elts = raw_ann.slice.elts
                if (
                    len(elts) == 2
                    and isinstance(elts[0], ast.Name)
                    and isinstance(elts[1], ast.Name)
                ):
                    return (elts[0].id, elts[1].id)
    return False


def parse_simple_binop(bin: ast.BinOp) -> list[str]:
    if isinstance(bin.left, ast.Name):
        if isinstance(bin.right, ast.Name):
            return [bin.left.id, bin.right.id]
        elif isinstance(bin.right, ast.BinOp):
            return [bin.left.id] + parse_simple_binop(bin.right)
    raise Exception("UnparseableBinop")


def multi_dict_detector(ass: ast.AnnAssign) -> tuple[str, list[str]] | Literal[False]:
    raw_ann = strip_optional(ass)
    if isinstance(raw_ann, ast.Subscript):
        if isinstance(raw_ann.value, ast.Name) and raw_ann.value.id == "dict":
            if isinstance(raw_ann.slice, ast.Tuple):
                elts = raw_ann.slice.elts
                if (
                    len(elts) == 2
                    and isinstance(elts[0], ast.Name)
                    and isinstance(elts[1], ast.BinOp)
                ):
                    try:
                        opts = parse_simple_binop(elts[1])
                        return (elts[0].id, opts)
                    except Exception as e:
                        return False
    return False


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
