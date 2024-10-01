import ast

from code_generator._class.__eq__.rq_or_op import is_if_target, make_test_if


def resolve__eq__(target_id: str, body: list[ast.stmt]) -> None:
    for dec in body:
        if isinstance(dec, ast.FunctionDef) and dec.name == "__eq__":
            for line in dec.body:
                if isinstance(line, ast.If):
                    if is_if_target(line, target_id):
                        return
            else:
                dec.body.insert(len(dec.body) - 1, make_test_if(target_id))
            return
    else:
        fun: ast.FunctionDef = ast.parse(
            "def __eq__(self,value:Any)->bool:\n\tif not isinstance(value,type(self)):\n\t\treturn False\n\treturn True"
        ).body[0]  # type: ignore
        fun.body.insert(len(fun.body) - 1, make_test_if(target_id))
        body.append(fun)
        return
