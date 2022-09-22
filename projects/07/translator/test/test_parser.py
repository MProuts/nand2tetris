import pytest

from parser import Parser

class TestParser:
    def test_emptyline(self):
        line = ''
        assert Parser.parse(line) == { 'blank': True }

    def test_blankline(self):
        line = '     '
        assert Parser.parse(line) == { 'blank': True }

    def test_comment(self):
        line = '// something helpful'
        assert Parser.parse(line) == { 'blank': True }

    def test_two_args(self):
        line = 'push constant 7'
        tokens = {
            'command': 'push',
            'arg1': 'constant',
            'arg2': '7'
        }
        assert Parser.parse(line) == tokens

    def test_one_arg(self):
        line = 'label foo'
        tokens = {
            'command': 'label',
            'arg1': 'foo',
            'arg2': None
        }
        assert Parser.parse(line) == tokens

    def test_zero_args(self):
        line = 'add'
        tokens = {
            'command': 'add',
            'arg1': None,
            'arg2': None
        }
        assert Parser.parse(line) == tokens

    # Fails to parse lines with extra non-comment characters
    def test_five_args(self):
        line = 'push constant 7 blah blah'
        tokens = {}
        assert Parser.parse(line) == tokens
