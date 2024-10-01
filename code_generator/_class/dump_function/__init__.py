import ast

from code_generator._class.dump_function.optional import is_target_if, make_if_statement
from code_generator._class.dump_function.required import is_target_ann, make_target_ann
from code_generator._class.utils import optional_detector


def resolve_dump(ass: ast.AnnAssign, target_id: str, body: list[ast.stmt]) -> None:
    is_optional = optional_detector(ass)

    for dec in body:
        if isinstance(dec, ast.FunctionDef) and dec.name == "dump":
            if is_optional:
                for line in dec.body:
                    if isinstance(line, ast.If) and is_target_if(line, target_id):
                        break
                else:
                    dec.body.insert(len(dec.body) - 1, make_if_statement(target_id))
            else:
                for line in dec.body:
                    if isinstance(line, ast.Assign) and is_target_ann(line, target_id):
                        break
                else:
                    dec.body.insert(len(dec.body) - 1, make_target_ann(target_id))
            return
    else:
        fun: ast.FunctionDef = ast.parse(
            "def dump(self,source:JSON_DICT)->JSON_DICT:\n\tif not source:\n\t\tsource=deepcopy(self.source)\n\treturn source"
        ).body[0]  # type: ignore
        fun.body.insert(len(fun.body) - 1, make_target_ann(target_id))
        body.append(fun)
