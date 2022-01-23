from enum import Enum, auto
from nis import match
from typing import Union


class AutoName(Enum):
    def _generate_next_value_(name, _, __, ___):
        return name


class TokenType(AutoName):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


class Token:
    def __init__(
        self, type: Union[TokenType, str], lexeme: str, literal: object, line: int
    ) -> None:
        type = TokenType(type)
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self) -> str:
        return f"{self.type.value} {self.lexeme} {self.literal}"


class Scanner:
    def __init__(self, source: str):
        self._source = source
        self.tokens = []
        self.line = 1
        self.start = 0
        self.current = 0

    def _is_at_end(self) -> bool:
        return self.current >= len(self._source)

    def _advance(self):
        char = self._source[self.current]
        self.current += 1
        return char

    def _add_token_literal(self, type: TokenType, literal: object):
        text = self._source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def _add_token(self, type: TokenType):
        self._add_token_literal(type, None)

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self._source[self.current] != expected:
            return False

        self.current += 1
        return True

    def _scan_token(self, lox_cls):
        char = self._advance()
        if char == "(":
            self._add_token(TokenType.LEFT_PAREN)
            return
        elif char == ")":
            self._add_token(TokenType.RIGHT_PAREN)
            return
        elif char == "{":
            self._add_token(TokenType.LEFT_BRACE)
            return
        elif char == "}":
            self._add_token(TokenType.RIGHT_BRACE)
            return
        elif char == ",":
            self._add_token(TokenType.COMMA)
            return
        elif char == ".":
            self._add_token(TokenType.DOT)
            return
        elif char == "-":
            self._add_token(TokenType.MINUS)
            return
        elif char == "+":
            self._add_token(TokenType.PLUS)
            return
        elif char == "*":
            self._add_token(TokenType.STAR)
            return
        elif char == "!":
            if self._match("="):
                self._add_token(TokenType.BANG_EQUAL)
            else:
                self._add_token(TokenType.BANG)
            return
        elif char == "=":
            if self._match("="):
                self._add_token(TokenType.EQUAL_EQUAL)
            else:
                self._add_token(TokenType.EQUAL)
            return
        elif char == ">":
            if self._match("="):
                self._add_token(TokenType.GREATER_EQUAL)
            else:
                self._add_token(TokenType.GREATER)
            return
        elif char == "<":
            if self._match("="):
                self._add_token(TokenType.LESS_EQUAL)
            else:
                self._add_token(TokenType.LESS)
            return
        elif char == "/":
            if self._match("/"):
                while self._peek() != "\n" and not self._is_at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
            return

        lox_cls.error(self.line, f"Unexpected character {char}")

    def _peek(self):
        if self._is_at_end():
            return "\0"
        return self._source[self.current]

    def scan_tokens(self, lox_cls) -> list[Token]:
        while not self._is_at_end():
            self.start = self.current
            self._scan_token(lox_cls)

        self.tokens.append(Token("EOF", "", None, self.line))
        return self.tokens
