from cmath import exp
from pylox.parser.expr import Expr, Binary, ExprVisitor, Grouping, Literal, Unary


class AstPrinter(ExprVisitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def paranthesis(self, name: str, *exprs: Expr) -> str:
        ret = [f"({name}"]
        for expr in exprs:
            ret.append(" ")
            ret.append(expr.accept(self))
        ret.append(")")
        return "".join(ret)

    def visit_unary(self, expr: Unary):
        return self.paranthesis(expr.operator.lexeme, expr.right)

    def visit_grouping(self, expr: Grouping):
        return self.paranthesis("group", expr.expression)

    def visit_literal(self, expr: Literal):
        if expr.value == None:
            return "nil"
        return str(expr.value)

    def visit_binary(self, expr: Binary):
        return self.paranthesis(expr.operator.lexeme, expr.left, expr.right)
