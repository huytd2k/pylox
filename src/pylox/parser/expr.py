# This file is auto generated
from __future__ import annotations
from abc import ABCMeta

from pylox.scanner.scanner import Token


class Expr(metaclass=ABCMeta):
    def accept(self, visitor: ExprVisitor):
        pass


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_unary(self)


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_grouping(self)


class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_literal(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_binary(self)


class ExprVisitor(metaclass=ABCMeta):
    def visit_unary(self, expr: Unary):
        pass

    def visit_grouping(self, expr: Grouping):
        pass

    def visit_literal(self, expr: Literal):
        pass

    def visit_binary(self, expr: Binary):
        pass