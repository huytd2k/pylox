# This file is auto generated
from __future__ import annotations
from abc import ABCMeta

from pylox.parser.expr import Expr


class Stmt(metaclass=ABCMeta):
    def accept(self, visitor: StmtVisitor):
        pass


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_expression(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_print(self)


class StmtVisitor(metaclass=ABCMeta):
    def visit_expression(self, stmt: Expression):
        pass

    def visit_print(self, stmt: Print):
        pass