from __future__ import annotations
from abc import ABCMeta
from enum import auto
from typing import TypeVar, Union

from helper.enum import AutoName

_T = TypeVar("_T")


class ExprVisitor(metaclass=ABCMeta):
    def visit(self, eppr: Expr):
        pass


class PrintVisitor(ExprVisitor):
    def visit(self, eppr: Expr):
        print()

    def visit_literal_expr(self, expr: Expr):
        print(expr.childs[0])

    def visit_binary_expr(self, expr: Expr):
        pass


class EpxrType(AutoName):
    BINARY = auto()
    GROUPING = auto()
    LITERAL = auto()
    UNARY = auto()


class Expr:
    def __repr__(self) -> str:
        pass

    def accept(self, visitor: ExprVisitor):
        visitor.visit(self)

    def __init__(
        self,
        type: Union[ExprVisitor, str],
        childs: list[Union[Expr, object]] = None,
    ) -> None:
        type = ExprVisitor(type)
        self.childs = childs or []
        self.type = type
