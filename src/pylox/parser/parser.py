from __future__ import annotations
from pylox.parser.expr import Binary, Expr, Grouping, Literal, Unary
from pylox.scanner.scanner import Token, TokenType


class ParsingError(Exception):
    def __init__(self, token: Token, msg: str) -> None:
        super().__init__(msg)
        self.token = token
        self.msg = msg


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0
        self.errors: list[ParsingError] = []

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _match(self, *token_types: TokenType) -> bool:
        for type in token_types:
            if self._check(type):
                self._advance()
                return True

    def _error(self, token: Token, msg: str):
        exp = ParsingError(token, msg)
        self.errors.append(exp)
        return exp

    def _consume(self, type: TokenType, msg: str):
        if self._check(type):
            return self._advance()
        raise self._error(self._peek(), msg)

    def _check(self, type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == type

    def _primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NIL):
            return Literal(None)
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)
        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after an expression")
            return Grouping(expr)
        raise self._error(self._peek(), "Expected expression!")

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _unary(self) -> Expr:
        if self._match(TokenType.MINUS, TokenType.BANG):
            expr = self._previous()
            return Unary(expr, self._unary())
        return self._primary()

    def _factor(self) -> Expr:
        expr = self._unary()
        while self._match(
            TokenType.STAR,
            TokenType.SLASH,
        ):
            opr = self._previous()
            right = self._unary()
            expr = Binary(expr, opr, right)
        return expr

    def _term(self) -> Expr:
        expr = self._factor()
        while self._match(
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            opr = self._previous()
            right = self._factor()
            expr = Binary(expr, opr, right)
        return expr

    def _comparision(self) -> Expr:
        expr = self._term()
        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            opr = self._previous()
            right = self._term()
            expr = Binary(expr, opr, right)
        return expr

    def _equality(self) -> Expr:
        expr = self._comparision()
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            opr = self._previous()
            right = self._comparision()
            expr = Binary(expr, opr, right)
        return expr

    def _ternary(self) -> Expr:
        """tenary -> equality ? equality : ternary | equality"""
        expr = self._equality()
        if self._match(TokenType.QUESTION_MARK):
            opr = self._previous()
            first = self._equality()
            colon = self._consume(TokenType.COLON, "Expected colon!")
            second = self._ternary()
            return Binary(expr, opr, Binary(first, colon, second))
        return expr

    def _expression(self) -> Expr:
        return self._ternary()

    def parse(self) -> Expr:
        try:
            self._expression()
        except ParsingError as e:
            return None
