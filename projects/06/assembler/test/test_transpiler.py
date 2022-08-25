from transpiler import Transpiler
from symbol_table import SymbolTable

import pytest

class TestTranspiler:
    # .transpile()
    # ===========
    def test_addr(self):
        binary = Transpiler.transpile({ 'addr': '123' }, {})
        expected = '000 0000001 111 011'.replace(' ', '')
        assert binary == expected

    def test_comp(self):
        tokens = { 'comp': 'D&A', 'dest': None, 'jump': None }
        binary = Transpiler.transpile(tokens, {})
        expected = '111 0000000 000 000'.replace(' ', '')
        assert binary == expected


    def test_dest_comp(self):
        tokens = { 'comp': 'D+1', 'dest': 'D', 'jump': None }
        binary = Transpiler.transpile(tokens, {})
        expected = '111 0011111 010 000'.replace(' ', '')
        assert binary == expected

    def test_comp_jump(self):
        tokens = { 'comp': '!M', 'dest': None, 'jump': 'JLE' }
        binary = Transpiler.transpile(tokens, {})
        expected = '111 1110001 000 110'.replace(' ', '')
        assert binary == expected

    def test_dest_comp_jump(self):
        tokens = { 'comp': '-1', 'dest': 'M', 'jump': 'JMP' }
        binary = Transpiler.transpile(tokens, {})
        expected = '111 0111010 001 111'.replace(' ', '')
        assert binary == expected

    def test_goto(self):
        symbol_table = SymbolTable()
        symbol_table.set('FOO', 5)
        binary = Transpiler.transpile({ 'addr': 'FOO' }, symbol_table)
        expected = '000 0000000 000 101'.replace(' ', '')
        assert binary == expected

    def test_variable(self):
        binary = Transpiler.transpile({ 'addr': 'FOO' }, SymbolTable())
        expected = '000 0000000 010 000'.replace(' ', '')
        assert binary == expected

        binary = Transpiler.transpile({ 'addr': 'BAR' }, SymbolTable())
        expected = '000 0000000 010 000'.replace(' ', '')
        assert binary == expected

    # .validate()
    # ===========
    def test_blank(self):
        with pytest.raises(ValueError):
            tokens = { 'blank': True }
            Transpiler.validate(tokens, {})

    def test_empty_tokens(self):
        with pytest.raises(ValueError):
            tokens = {}
            Transpiler.validate(tokens, {})

    def test_invalid_comp(self):
        with pytest.raises(ValueError):
            tokens = { 'comp': 'foo' }
            Transpiler.validate(tokens, {})

    def test_blank_comp(self):
        with pytest.raises(ValueError):
            tokens = { 'comp': '' }
            Transpiler.validate(tokens, {})

    def test_missing_comp(self):
        with pytest.raises(ValueError):
            tokens = { 'dest': 'M', 'jump': 'JMP' }
            Transpiler.validate(tokens, {})

    def test_invalid_dest(self):
        with pytest.raises(ValueError):
            tokens = { 'comp': '0', 'dest': 'bar' }
            Transpiler.validate(tokens, {})

    def test_invalid_jump(self):
        with pytest.raises(ValueError):
            tokens = { 'comp': '0', 'jump': 'baz' }
            Transpiler.validate(tokens, {})
