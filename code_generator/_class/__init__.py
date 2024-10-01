import ast
import os
import ast_comments

from code_generator._class.__eq__ import resolve__eq__
from code_generator._class.dump_function import resolve_dump
from code_generator._class.init_function import resolve__init__


def parse_file(dir: str) -> None:
    with open(dir) as infile:
        doc: ast.Module = ast_comments.parse(infile.read())  # type: ignore
    for entry in doc.body:
        if isinstance(entry, ast.ClassDef):
            for line in entry.body:
                if isinstance(line, ast.AnnAssign) and isinstance(
                    line.target, ast.Name
                ):
                    if line.target.id.startswith("_"):
                        resolve__init__(line, line.target.id[1:], entry.body)
                        resolve_dump(line, line.target.id[1:], entry.body)
                        resolve__eq__(line.target.id[1:], entry.body)
    with open(dir, "w") as outfile:
        outfile.write(ast_comments.unparse(doc))


if __name__ == "__main__":
    import glob

    # root_dir needs a trailing slash (i.e. /root/dir/)
    for filename in glob.iglob(
        os.path.join(os.path.abspath(os.getcwd()) + "\\objectopenapi\\") + "**/*.py",
        recursive=True,
    ):
        print(filename)
