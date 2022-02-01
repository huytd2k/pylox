# This file is auto generated
from __future__ import annotations
from abc import ABCMeta

from pylox.scanner.scanner import Token


class Expr(metaclass=ABCMeta):
    def accept(self, visitor: ExprVisitor):
        pass


class Assign(Expr):
    def __init__(self, name: Token, expr: Expr):
        self.name = name
        self.expr = expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_assign(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_binary(self)


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


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_unary(self)


class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_variable(self)


class ExprVisitor(metaclass=ABCMeta):
    def visit_assign(self, expr: Assign):
        pass

    def visit_binary(self, expr: Binary):
        pass

    def visit_grouping(self, expr: Grouping):
        pass

    def visit_literal(self, expr: Literal):
        pass

    def visit_unary(self, expr: Unary):
        pass

    def visit_variable(self, expr: Variable):
        pass
