import pylox.scanner.scanner as s


def assert_tokens_equal(f_tokens: list[s.Token], s_tokens: list[s.Token]):
    assert len(f_tokens) == len(s_tokens)
    for i in range(len(f_tokens)):
        assert f_tokens[i].type == s_tokens[i].type
        assert f_tokens[i].lexeme == s_tokens[i].lexeme
        assert f_tokens[i].literal == s_tokens[i].literal


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
