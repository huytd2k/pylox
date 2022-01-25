from pylox.parser.ast_printer import AstPrinter
from pylox.parser.expr import Binary, Grouping, Literal, Unary
from pylox.scanner.scanner import Token, TokenType


def test_ast_printer():
    printer = AstPrinter()
    ret = printer.print(
        Binary(
            left=Literal(1),
            operator=Token(TokenType.PLUS, "+", None, 1),
            right=Literal(3),
        ),
    )
    assert ret == "(+ 1 3)"

    ret = printer.print(
        Binary(
            Unary(
                Token(TokenType.MINUS, "-", None, 1),
                Literal(123),
            ),
            Token(TokenType.STAR, "*", None, 1),
            Grouping(
                Literal(45.67),
            ),
        )
    )
    assert ret == "(* (- 123) (group 45.67))"
