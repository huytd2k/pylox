#! python
import sys
import os

EXPR_DEFS = [
    "Assign : name Token, expr Expr",
    "Binary : left Expr, operator Token, right Expr",
    "Grouping : expression Expr",
    "Literal : value object",
    "Unary : operator token, right Expr",
    "Variable: name Token",
]

STMT_DEFS = [
    "Expression : expression Expr",
    "Print : expression Expr",
    "Var : name Token, init Expr",
    "Block: statements list[Stmt]",
]


def declare_imports() -> str:
    return """\
# This file is auto generated
from __future__ import annotations
from abc import ABCMeta

from pylox.scanner.scanner import Token
from pylox.parser.expr import Expr"""


def newlines(num=1):
    return "\n" * num


def define_abc_expr(basename: str) -> str:
    return f"""\
class {basename}(metaclass=ABCMeta):
    def accept(self, visitor: {basename}Visitor):
        pass"""


def define_expr(defi: str, basename: str) -> str:
    name = defi.split(":")[0].strip()
    fields = defi.split(":")[1].strip().split(",")
    fields = [f.strip().replace(" ", ": ") for f in fields]
    props = [f.split(":")[0] for f in fields]
    constructor_implement = "\n".join(f"        self.{prop} = {prop}" for prop in props)
    return f"""\
class {name}({basename}):
    def __init__(self, {", ".join(fields)}):
{constructor_implement}

    def accept(self, visitor: {basename}Visitor):
        return visitor.visit_{name.lower()}(self)"""


def define_vistor(names: list[str], basename: str):
    def def_method(name: str):
        return f"""\
    def visit_{name.lower()}(self, {basename.lower()}: {name}):
        pass"""

    methods = [def_method(name) for name in names]
    methods = newlines(2).join(methods)

    return f"""\
class {basename}Visitor(metaclass=ABCMeta):
{methods}"""


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
            define_abc_expr(basename),
            newlines(3),
        ]
    )
    # fmt: on
    defs = STMT_DEFS
    names = [def_.split(":")[0].strip() for def_ in defs]
    defs = newlines(3).join([define_expr(defi, basename) for defi in defs])
    vistor_def = define_vistor(names, basename)
    source += defs
    source += newlines(3)
    source += vistor_def
    with open(file_path, "w") as f:
        f.write(source)


if __name__ == "__main__":
    main()
