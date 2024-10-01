"""
source['variable'] = self.variable

<ast.Assign object at 0x0000026B96FA22C0>
targets
item:0
        <ast.Subscript object at 0x0000026B96FA3400>
        ctx:<ast.Store object at 0x0000026B92EB92D0>
                <ast.Store object at 0x0000026B92EB92D0>
        slice:<ast.Constant object at 0x0000026B971BF8E0>
                <ast.Constant object at 0x0000026B971BF8E0>
                kind:None
                        None
                n:variable
                        variable
                s:variable
                        variable
                value:variable
                        variable
        value:<ast.Name object at 0x0000026B96DA70A0>
                <ast.Name object at 0x0000026B96DA70A0>
                ctx:<ast.Load object at 0x0000026B92EB9360>
                        <ast.Load object at 0x0000026B92EB9360>
                id:source
                        source
type_comment:None
        None
value:<ast.Attribute object at 0x0000026B971BDC60>
        <ast.Attribute object at 0x0000026B971BDC60>
        attr:variable
                variable
        ctx:<ast.Load object at 0x0000026B92EB9360>
                <ast.Load object at 0x0000026B92EB9360>
        value:<ast.Name object at 0x0000026B971BD8D0>
                <ast.Name object at 0x0000026B971BD8D0>
                ctx:<ast.Load object at 0x0000026B92EB9360>
                        <ast.Load object at 0x0000026B92EB9360>
                id:self
                        self
"""

import ast


def is_target_ann(ass: ast.Assign, target_id: str):
    if isinstance(ass.targets[0], ast.Subscript):
        target = ass.targets[0]
        if isinstance(target.slice, ast.Constant):
            if target.slice.value == target_id:
                if isinstance(target.value, ast.Name):
                    if target.value.id == "source":
                        return True
    return False


def make_target_ann(target_id: str):
    return ast.parse(f"source['{target_id}'] = self.{target_id}").body[0]
