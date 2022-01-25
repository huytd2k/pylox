# This file is auto generated
from __future__ import annotations
from abc import ABCMeta

from pylox.scanner.scanner import Token


class Expr(metaclass=ABCMeta):
    pass


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression


class Literal(Expr):
    def __init__(self, value: object):
        self.value = value


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right
