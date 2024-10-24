"""
if self.variable is not None:
    source[variable] = self.variable
elif remove_unset:
    source.pop(variable,None)
<ast.If object at 0x0000026B96FA1870>
body
item:0
        <ast.Assign object at 0x0000026B96FA2B30>
        targets
        item:0
                <ast.Subscript object at 0x0000026B96FA2230>
                ctx:<ast.Store object at 0x0000026B92EB92D0>
                        <ast.Store object at 0x0000026B92EB92D0>
                slice:<ast.Name object at 0x0000026B96FA1BA0>
                        <ast.Name object at 0x0000026B96FA1BA0>
                        ctx:<ast.Load object at 0x0000026B92EB9360>
                        id:variable
                value:<ast.Name object at 0x0000026B96FA1D50>
                        <ast.Name object at 0x0000026B96FA1D50>
                        ctx:<ast.Load object at 0x0000026B92EB9360>
                        id:source
        type_comment:None
                None
        value:<ast.Attribute object at 0x0000026B96FA1510>
                <ast.Attribute object at 0x0000026B96FA1510>
                attr:variable
                        variable
                ctx:<ast.Load object at 0x0000026B92EB9360>
                        <ast.Load object at 0x0000026B92EB9360>
                value:<ast.Name object at 0x0000026B96FA3010>
                        <ast.Name object at 0x0000026B96FA3010>
                        ctx:<ast.Load object at 0x0000026B92EB9360>
                        id:self
orelse
item:0
        <ast.If object at 0x0000026B96FA1CF0>
        body
        item:0
                <ast.Expr object at 0x0000026B96FA3880>
                value:<ast.Call object at 0x0000026B96FA32B0>
                        <ast.Call object at 0x0000026B96FA32B0>
                        args
                        item:0
                        item:1
                        func:<ast.Attribute object at 0x0000026B96FA1ED0>
                        keywords
        orelse
        test:<ast.Name object at 0x0000026B96FA1F90>
                <ast.Name object at 0x0000026B96FA1F90>
                ctx:<ast.Load object at 0x0000026B92EB9360>
                        <ast.Load object at 0x0000026B92EB9360>
                id:remove_unset
                        remove_unset
test:<ast.Compare object at 0x0000026B96FA1840>
        <ast.Compare object at 0x0000026B96FA1840>
        comparators
        item:0
                <ast.Constant object at 0x0000026B96FA1CC0>
                kind:None
                        None
                n:None
                        None
                s:None
                        None
                value:None
                        None
        left:<ast.Attribute object at 0x0000026B96FA2140>
                <ast.Attribute object at 0x0000026B96FA2140>
                attr:variable
                        variable
                ctx:<ast.Load object at 0x0000026B92EB9360>
                        <ast.Load object at 0x0000026B92EB9360>
                value:<ast.Name object at 0x0000026B96FA15D0>
                        <ast.Name object at 0x0000026B96FA15D0>
                        ctx:<ast.Load object at 0x0000026B92EB9360>
                        id:self
        ops
        item:0
                <ast.IsNot object at 0x0000026B92EBBE50>
"""

import ast

from code_generator._class.dump_function.utils import make_dict_dump
from code_generator._class.utils import multi_dict_detector, simple_dict_detector


def is_target_if(fi: ast.If, target_id: str) -> bool:
    if isinstance(fi.test, ast.Compare):
        test = fi.test
        if isinstance(test.ops[0], ast.IsNot):
            if isinstance(test.left, ast.Attribute):
                if isinstance(test.left.value, ast.Name):
                    return test.left.attr == target_id and test.left.value.id == "self"
    return False


def make_if_statement(ass: ast.AnnAssign, target_id: str) -> ast.stmt:
    fi: ast.If = ast.parse(
        f"if self.{target_id} is not None:\n\tsource['{target_id}'] = self.{target_id}\nelif remove_unset:\n\tsource.pop('{target_id}',None)"
    ).body[0]  # type:ignore
    if simple_dict_detector(ass) or multi_dict_detector(ass):
        fi.body = [make_dict_dump(target_id)]
    return fi
