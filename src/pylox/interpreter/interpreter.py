from pylox.parser.stmt import Expression, Print, Stmt, StmtVisitor, Var, Block
from pylox.parser.expr import (
    Assign,
    Binary,
    Expr,
    ExprVisitor,
    Grouping,
    Literal,
    Unary,
    Variable,
)
from pylox.scanner.scanner import TokenType, Token
from .environment import Environment


class RuntimeError(Exception):
    def __init__(self, token: Token, msg: str) -> None:
        super().__init__(msg)
        self.token = token
        self.msg = msg


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self) -> None:
        self._env = Environment()

    def _eval(self, expr: Expr) -> object:
        return expr.accept(self)

    def _execute_blocks(self, statements: list[Stmt], env: Environment):
        previous = self._env
        try:
            self._env = env
            for stmt in statements:
                self.execute(stmt)
        finally:
            self._env = previous

    def visit_block(self, stmt: Block):
        self._execute_blocks(stmt.statements, Environment(self._env))
        return

    def visit_assign(self, expr: Assign):
        val = self._eval(expr.expr)
        self._env.assign(expr.name, val)
        return val

    def visit_var(self, stmt: Var):
        init_val = None
        if stmt.init is not None:
            init_val = self._eval(stmt.init)

        self._env.define(stmt.name.lexeme, init_val)

    def visit_variable(self, expr: Variable):
        return self._env.get(expr.name)

    def visit_expression(self, stmt: Expression):
        self._eval(stmt.expression)
        return

    def visit_print(self, stmt: Print):
        print(self._eval(stmt.expression))

    def interpret(self, stmts: list[Stmt]):
        try:
            for stmt in stmts:
                self.execute(stmt)
        except RuntimeError as e:
            raise

    def execute(self, stmt: Stmt):
        return stmt.accept(self)

    def _is_truthy(self, obj: object) -> bool:
        if isinstance(obj, float):
            return obj != 0
        if isinstance(obj, str):
            return obj != ""
        if isinstance(obj, bool):
            return obj
        if obj is None:
            return False
        return True

    def visit_unary(self, expr: Unary) -> object:
        right_val = self._eval(expr.right)
        if expr.operator.type == TokenType.MINUS:
            return -float(right_val)
        if expr.operator.type == TokenType.BANG:
            return not self._is_truthy(right_val)

        return None

    def visit_grouping(self, expr: Grouping):
        return self._eval(expr.expression)

    def visit_literal(self, expr: Literal):
        return expr.value

    def _types_equal(self, a: TokenType, b: TokenType):
        return a.value == b.value

    def visit_binary(self, expr: Binary):
        left = self._eval(expr.left)
        right = self._eval(expr.right)
        if self._types_equal(expr.operator.type, TokenType.MINUS):
            return float(left) - float(right)
        if self._types_equal(expr.operator.type, TokenType.STAR):
            return float(left) * float(right)
        if self._types_equal(expr.operator.type, TokenType.SLASH):
            return float(left) / float(right)
        if self._types_equal(expr.operator.type, TokenType.PLUS):
            return left + right
        if self._types_equal(expr.operator.type, TokenType.GREATER):
            return float(left) > float(right)
        if self._types_equal(expr.operator.type, TokenType.GREATER_EQUAL):
            return float(left) >= float(right)
        if self._types_equal(expr.operator.type, TokenType.LESS):
            return float(left) < float(right)
        if self._types_equal(expr.operator.type, TokenType.LESS_EQUAL):
            return float(left) <= float(right)
        if self._types_equal(expr.operator.type, TokenType.EQUAL_EQUAL):
            return left == right
        if self._types_equal(expr.operator.type, TokenType.BANG_EQUAL):
            return left != right
        if self._types_equal(expr.operator.type, TokenType.QUESTION_MARK):
            if self._is_truthy(left):
                return self._eval(expr.right.left)
            else:
                return self._eval(expr.right.right)
