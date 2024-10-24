"""
if self.var != value.var:
    return False

<ast.If object at 0x0000026B9708E920>
body
item:0
        <ast.Return object at 0x0000026B971BDD80>
        value:<ast.Constant object at 0x0000026B971BF8B0>
                <ast.Constant object at 0x0000026B971BF8B0>
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
test:<ast.Compare object at 0x0000026B9708EEC0>
        <ast.Compare object at 0x0000026B9708EEC0>
        comparators
        item:0
                <ast.Attribute object at 0x0000026B971BE260>
                attr:var
                        var
                ctx:<ast.Load object at 0x0000026B92EB9360>
                        <ast.Load object at 0x0000026B92EB9360>
                value:<ast.Name object at 0x0000026B971BC280>
                        <ast.Name object at 0x0000026B971BC280>
                        ctx:<ast.Load object at 0x0000026B92EB9360>
                        id:value
        left:<ast.Attribute object at 0x0000026B97191F30>
                <ast.Attribute object at 0x0000026B97191F30>
                attr:var
                        var
                ctx:<ast.Load object at 0x0000026B92EB9360>
                        <ast.Load object at 0x0000026B92EB9360>
                value:<ast.Name object at 0x0000026B97193940>
                        <ast.Name object at 0x0000026B97193940>
                        ctx:<ast.Load object at 0x0000026B92EB9360>
                        id:self
        ops
        item:0
                <ast.NotEq object at 0x0000026B92EBBC10>
"""

import ast

from code_generator._class.utils import multi_dict_detector, simple_dict_detector


def is_if_target(fi: ast.If, target_id: str) -> bool:
    if isinstance(fi.test, ast.Compare):
        test = fi.test
        if isinstance(test.comparators[0], ast.Attribute):
            comp = test.comparators[0]
            if comp.attr == target_id:
                if isinstance(comp.value, ast.Name):
                    if comp.value.id == "value":
                        if isinstance(test.left, ast.Attribute):
                            left = test.left
                            if isinstance(left.value, ast.Name):
                                if left.attr == target_id and left.value.id == "self":
                                    return True

    return False


def make_test_if(ass: ast.AnnAssign, target_id: str):
    if simple_dict_detector(ass) or multi_dict_detector(ass):
        return ast.parse(
            f"if set(self.{target_id}.keys()) == set(value.{target_id}.keys()):\n\tfor key in self.{target_id}:\n\t\tif value.{target_id}[key] != self.{target_id}[key]:\n\t\t\treturn False\nelse:\n\treturn False"
        ).body[0]
    return ast.parse(f"if self.{target_id} != value.{target_id}:\n\treturn False").body[
        0
    ]
