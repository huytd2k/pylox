from __future__ import annotations
import pylox.interpreter.interpreter as i
from pylox.scanner.scanner import Token


class Environment:
    def __init__(self, enclosing: Environment = None) -> None:
        self._values = {}
        self._enclosing = enclosing

    def define(self, name: str, val: object):
        self._values[name] = val

    def assign(self, name: Token, val: object):
        if name.lexeme in self._values:
            self._values[name.lexeme] = val
            return

        if self._enclosing is not None:
            return self._enclosing.assign(name, val)

        raise i.RuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def get(self, name: Token):
        if name.lexeme in self._values:
            return self._values[name.lexeme]
        if self._enclosing is not None:
            return self._enclosing.get(name)

        raise i.RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
