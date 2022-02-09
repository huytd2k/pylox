# This file is auto generated
from __future__ import annotations
from abc import ABCMeta

from pylox.scanner.scanner import Token
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


class Var(Stmt):
    def __init__(self, name: Token, init: Expr):
        self.name = name
        self.init = init

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_var(self)


class Block(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_block(self)


class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_if(self)


class While(Stmt):
    def __init__(self, condition: Expr, stmt: Stmt):
        self.condition = condition
        self.stmt = stmt

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_while(self)


class StmtVisitor(metaclass=ABCMeta):
    def visit_expression(self, stmt: Expression):
        pass

    def visit_print(self, stmt: Print):
        pass

    def visit_var(self, stmt: Var):
        pass

    def visit_block(self, stmt: Block):
        pass

    def visit_if(self, stmt: If):
        pass

    def visit_while(self, stmt: While):
        pass