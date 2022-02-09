import sys
from interpreter.interpreter import Interpreter, RuntimeError

import pylox.scanner.scanner as s
from pylox.parser.parser import Parser


class Lox:
    had_error = False
    had_runtime_error = False

    @classmethod
    def run(cls, source: str):
        scanner = s.Scanner(source)

        tokens = scanner.scan_tokens()
        for err in scanner.errors:
            Lox.error(err.line, err.msg)
        parser = Parser(tokens)
        stmts = parser.parse()
        for err in parser.errors:
            Lox.parse_error(err.token, err.msg)

        if cls.had_error:
            return None
        try:
            Interpreter().interpret(stmts)
        except RuntimeError as e:
            Lox.runtime_error(e)
            sys.exit(70)

    @classmethod
    def runtime_error(cls, e: RuntimeError):
        cls.had_runtime_error = True
        print(f"{e.msg}\n[line {e.token.line}]", file=sys.stderr)

    @classmethod
    def run_file(cls, path: str):
        print(f"Running in path {path}")
        with open(path, "r") as f_in:
            Lox.run(f_in.read())
        if cls.had_error:
            print("ERR!")
            sys.exit(65)

    @classmethod
    def run_prompt(cls):
        while True:
            print("> ", end="")
            line = input()
            if not line:
                break
            Lox.run(line)
            cls.had_error = False

    @classmethod
    def main(cls):
        if len(sys.argv) > 2:
            print("Usage: pylox [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            Lox.run_file(sys.argv[-1])
        else:
            Lox.run_prompt()

    @classmethod
    def error(cls, line: int, message: str):
        Lox.report(line, "", message)

    @classmethod
    def parse_error(cls, token: s.Token, message: str):
        if token.type.value == s.TokenType.EOF:
            Lox.report(token.line, "at end", message)
        else:
            Lox.report(token.line, f"at {token.lexeme}", message)

    @classmethod
    def report(cls, line: int, where: str, message: str):
        print(f"[line {line}] Error {where} : {message}")
        cls.had_error = True
