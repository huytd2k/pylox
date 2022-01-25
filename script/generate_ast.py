#! python
import sys
import os
from re import sub


def declare_imports() -> str:
    return """\
# This file is auto generated
from __future__ import annotations
from abc import ABCMeta

from pylox.scanner.scanner import Token"""


def newlines(num=1):
    return "\n" * num


def define_abc_expr() -> str:
    return f"""\
class Expr(metaclass=ABCMeta):
    pass"""


def define_expr(defi: str) -> str:
    name = defi.split(":")[0].strip()
    fields = defi.split(":")[1].strip().split(",")
    fields = [f.strip().replace(" ", ": ") for f in fields]
    props = [f.split(":")[0] for f in fields]
    constructor_implement = "\n".join(f"        self.{prop} = {prop}" for prop in props)
    return f"""\
class {name}(Expr):
    def __init__(self, {", ".join(fields)}):
{constructor_implement}"""


def main():
    args = sys.argv
    if len(args) != 3:
        print("Usage: generate_ast [path] [basename]")
        sys.exit(1)
    path, basename = args[-2], args[-1]
    if not os.path.isdir(path):
        print(f"Invalid path {path}")
        sys.exit(1)
    file_path = os.path.join(path, f"{basename.lower()}.py")
    print(f"Start generating ast def at: {file_path}")
    # fmt: off
    source = "".join(
        [
            declare_imports(),
            newlines(3),
            define_abc_expr(),
            newlines(3),
        ]
    )
    defs = [
        "Unary : operator Token, right Expr",
        "Grouping : expression Expr",
        "Literal : value object",
        "Binary : left Expr, operator Token, right Expr",
    ]
    # fmt: on
    defs = newlines(3).join([define_expr(defi) for defi in defs])
    source += defs
    source += newlines()
    with open(file_path, "w") as f:
        f.write(source)


if __name__ == "__main__":
    main()
