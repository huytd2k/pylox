import pylox.interpreter.interpreter as i
from pylox.scanner.scanner import Token


class Environment:
    def __init__(self) -> None:
        self._values = {}

    def define(self, name: str, val: object):
        self._values[name] = val

    def assign(self, name: Token, val: object):
        if name.lexeme in self._values:
            self._values[name.lexeme] = val
            return

        raise i.RuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def get(self, name: Token):
        if name.lexeme in self._values:
            return self._values[name.lexeme]

        raise i.RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
