import pytest
import io
import dict2xml

from jack_tokenizer import JackTokenizer

class TestJackTokenizer:

    def test_empty(self):
        string_io = io.StringIO("")
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == []

    def test_whitespace(self):
        string_io = io.StringIO("     ")
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == []

    def test_keyword(self):
        string_io = io.StringIO("class")
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == [
            { "type": "keyword", "value": "class" }
        ]

    def test_keywords(self):
        string_io = io.StringIO("function boolean while")
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == [
            { "type": "keyword", "value": "function" },
            { "type": "keyword", "value": "boolean" },
            { "type": "keyword", "value": "while" },
        ]

    def test_symbol(self):
        string_io = io.StringIO("{")
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == [
            { "type": "symbol", "value": "{" }
        ]

    def test_symbols(self):
        string_io = io.StringIO("([])")
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == [
            { "type": "symbol", "value": "(" },
            { "type": "symbol", "value": "[" },
            { "type": "symbol", "value": "]" },
            { "type": "symbol", "value": ")" },
        ]

    def test_symbol_encoding(self):
        string_io = io.StringIO('<>&')
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == [
            { "type": "symbol", "value": "&lt;" },
            { "type": "symbol", "value": "&gt;" },
            { "type": "symbol", "value": "&amp;" },
        ]



    def test_keywords_symbols_whitespace(self):
        string_io = io.StringIO("  ([class])  ")
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == [
            { "type": "symbol", "value": "(" },
            { "type": "symbol", "value": "[" },
            { "type": "keyword", "value": "class" },
            { "type": "symbol", "value": "]" },
            { "type": "symbol", "value": ")" },
        ]

    def test_integer_constants(self):
        string_io = io.StringIO("1234")
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == [
            { "type": "integer_constant", "value": "1234" },
        ]

    # Only valid between 0 and 32767
    def test_invalid_integer(self):
        string_io = io.StringIO("32768")
        tokenizer = JackTokenizer(string_io)
        with pytest.raises(ValueError):
            tokenizer._tokens()

    def test_string_constant(self):
        string_io = io.StringIO('"once upon a time..."')
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == [
            { "type": "string_constant", "value": "once upon a time..." },
        ]

    def test_identifier(self):
        string_io = io.StringIO("_foobar123")
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == [
            { "type": "identifier", "value": "_foobar123" },
        ]

    def test_if_clause(self):
        string_io = io.StringIO('if (x < 0) { let state = "negative"; }')
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == [
            { "type": "keyword", "value": "if" },
            { "type": "symbol", "value": "(" },
            { "type": "identifier", "value": "x" },
            { "type": "symbol", "value": "&lt;" },
            { "type": "integer_constant", "value": "0" },
            { "type": "symbol", "value": ")" },
            { "type": "symbol", "value": "{" },
            { "type": "keyword", "value": "let" },
            { "type": "identifier", "value": "state" },
            { "type": "symbol", "value": "=" },
            { "type": "string_constant", "value": "negative" },
            { "type": "symbol", "value": ";" },
            { "type": "symbol", "value": "}" },
        ]

    def test_line_comment(self):
        string_io = io.StringIO("// comment\n1234")
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == [
            { "type": "integer_constant", "value": "1234" },
        ]

    def test_block_comment(self):
        string_io = io.StringIO("/* comment\n1234 */\nfoo")
        tokenizer = JackTokenizer(string_io)
        assert tokenizer._tokens() == [
            { "type": "identifier", "value": "foo" },
        ]

    def test_error(self):
        string_io = io.StringIO("🐍")
        tokenizer = JackTokenizer(string_io)
        with pytest.raises(ValueError):
            assert tokenizer._tokens()
