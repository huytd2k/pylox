from enum import auto
from typing import Union

from helper.enum import AutoName


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


RESERVED_WORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "true": TokenType.TRUE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


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
        return f"Token (type={self.type.value}, lexeme={self.lexeme}, literal={self.literal})"


class ScanningError(Exception):
    def __init__(self, msg: str, line: int) -> None:
        super().__init__(msg)
        self.line = line
        self.msg = msg


class Scanner:
    def __init__(self, source: str, tolerant=True):
        self._source = source
        self.tokens = []
        self.line = 1
        self.start = 0
        self.current = 0
        self._tolerant = tolerant
        self.errors: list[ScanningError] = []

    def _error(self, msg: str):
        err = ScanningError(msg, self.line)
        if not self._tolerant:
            raise err
        else:
            self.errors.append(err)

    def _is_at_end(self, offset=0) -> bool:
        return self.current + offset >= len(self._source)

    def _advance(self, step=1):
        char = self._source[self.current]
        self.current += step
        return char

    def _add_token(self, type: TokenType, literal: object = None):
        text = self._source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self._source[self.current] != expected:
            return False

        self.current += 1
        return True

    def _scan_token(self, tolarent=True):
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
        elif char == ";":
            self._add_token(TokenType.SEMICOLON)
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
                self._inline_comment()
            elif self._match("*"):
                self._block_comment()
            else:
                self._add_token(TokenType.SLASH)
            return
        elif char in (" ", "\t", "\r"):
            return
        elif char in ("\n"):
            self.line += 1
            return
        elif char == '"':
            self._string()
            return
        elif self._is_digit(char):
            self._number()
            return
        elif self._is_alpha(char):
            self._identifier()
            return

        self._error(f"Unexpected character {char}")

    def _inline_comment(self):
        while self._peek() != "\n" and not self._is_at_end():
            self._advance()

    def _block_comment(self):
        while (
            self._peek() != "*" or self._peek(offset=1) != "/"
        ) and not self._is_at_end(offset=1):
            if self._peek() == "\n":
                self.line += 1
            self._advance()
        if self._is_at_end(offset=1):
            self._error("Unterminated block comment")
            return
        self._advance(step=2)

    def _identifier(self):
        while self._is_alpha_numeric(self._peek()):
            self._advance()

        value = self._source[self.start : self.current]
        if value in RESERVED_WORDS:
            self._add_token(RESERVED_WORDS[value])
        else:
            self._add_token(TokenType.IDENTIFIER)

    def _is_digit(self, char: str):
        return ord(char) >= ord("0") and ord(char) <= ord("9")

    def _is_alpha(self, char: str):
        return (
            (ord(char) >= ord("a") and ord(char) <= ord("z"))
            or (ord(char) >= ord("A") and ord(char) <= ord("Z"))
            or char == "_"
        )

    def _is_alpha_numeric(self, char: str):
        return self._is_digit(char) or self._is_alpha(char)

    def _number(self):
        while self._is_digit(self._peek()):
            self._advance()

        if self._peek() == "." and self._is_digit(self._peek(offset=1)):
            self._advance()
            while self._is_digit(self._peek()):
                self._advance()

        self._add_token(
            TokenType.NUMBER, float(self._source[self.start : self.current])
        )

    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self.line += 1
            self._advance()

        if self._is_at_end():
            self._error("Unterminated string.")
            return

        self._advance()
        value = self._source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, value)

    def _peek(self, offset=0):
        if self._is_at_end(offset):
            return "\0"
        return self._source[self.current + offset]

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        self.tokens.append(Token("EOF", "", None, self.line))
        return self.tokens
