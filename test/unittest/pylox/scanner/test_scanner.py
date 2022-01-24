import pytest
import pylox.scanner.scanner as s


def assert_tokens_equal(f_tokens: list[s.Token], s_tokens: list[s.Token]):
    assert len(f_tokens) == len(s_tokens)
    for i in range(len(f_tokens)):
        assert f_tokens[i].type == s_tokens[i].type
        assert f_tokens[i].lexeme == s_tokens[i].lexeme
        assert f_tokens[i].literal == s_tokens[i].literal


# fmt: off
TEST_SOURCE = \
"""\
a = 5;
()[] \\ an inline comment
+-*;
/* a block comment
this cant span line */
"""\
# fmt: on

# fmt: off
UNTERMINATED_BLOCK_COMMENT = \
"""\
a = 5;
/* a block comment
this cant span line
"""\
# fmt: on

def test_scanner():
    scanner = s.Scanner("(){}")
    tokens = scanner.scan_tokens()
    tokens_ = [
        s.Token(s.TokenType.LEFT_PAREN, "(", None, 0),
        s.Token(s.TokenType.RIGHT_PAREN, ")", None, 0),
        s.Token(s.TokenType.LEFT_BRACE, "{", None, 0),
        s.Token(s.TokenType.RIGHT_BRACE, "}", None, 0),
        s.Token(s.TokenType.EOF, "", None, 0),
    ]
    assert_tokens_equal(tokens, tokens_)

    scanner = s.Scanner(TEST_SOURCE)
    tokens = scanner.scan_tokens()

    with pytest.raises(s.ScanningError):
        # Unterminated string
        scanner = s.Scanner('a = "abcd', tolerant=False)
        scanner.scan_tokens()

    with pytest.raises(s.ScanningError):
        # Unterminated string
        scanner = s.Scanner(UNTERMINATED_BLOCK_COMMENT, tolerant=False)
        scanner.scan_tokens()
