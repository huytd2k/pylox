import sys
from interpreter.interpreter import Interpreter
from parser.ast_printer import AstPrinter

import pylox.scanner.scanner as s
from pylox.parser.parser import Parser, ParsingError


class Lox:
    hadError = False

    @classmethod
    def run(cls, source: str):
        scanner = s.Scanner(source)

        tokens = scanner.scan_tokens()
        for err in scanner.errors:
            Lox.error(err.line, err.msg)
        parser = Parser(tokens)
        expr = parser._expression()
        for err in parser.errors:
            Lox.parse_error(err.token, err.msg)

        if cls.hadError:
            return None
        print(AstPrinter().print(expr))
        print(Interpreter()._eval(expr))

    @classmethod
    def run_file(cls, path: str):
        print(f"Running in path {path}")
        with open(path, "r") as f_in:
            Lox.run(f_in.read())
        if cls.hadError:
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
            cls.hadError = False

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
        cls.hadError = True
