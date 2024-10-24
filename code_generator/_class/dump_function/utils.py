import ast


def make_dict_dump(target_id: str):
    return ast.parse(
        f"source['{target_id}'] = {'{'}k:self.{target_id}[k].dump({{}}) for k in self.{target_id}{'}'}"
    ).body[0]
