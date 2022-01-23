import sys

import pylox.scanner.scanner as s


class Lox:
    hadError = False

    @classmethod
    def run(cls, source: str):
        scanner = s.Scanner(source)

        for token in scanner.scan_tokens(cls):
            print(token)

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
        print(sys.argv)
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
    def report(cls, line: int, where: str, message: str):
        print(f"[line {line}] Error {where} : {message}")
        cls.hadError = True
