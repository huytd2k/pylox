from cmath import exp
from pylox.parser.expr import Binary, Expr, ExprVisitor, Grouping, Literal, Unary
from scanner.scanner import Token, TokenType


class Interpreter(ExprVisitor):
    def _eval(self, expr: Expr) -> object:
        return expr.accept(self)

    def _is_truthy(obj: object) -> bool:
        if isinstance(float, obj):
            return obj != 0
        if isinstance(str, obj):
            return obj != ""
        if isinstance(bool, obj):
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
            if self._is_truthy(self._eval(left)):
                return self._eval(expr.right.left)
            else:
                return self._eval(expr.right.right)
