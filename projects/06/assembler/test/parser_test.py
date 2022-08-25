import pytest

from parser import Parser

class TestParser:
    def test_emptyline(self):
        line = ''
        assert Parser.parse(line) == { 'blank': True }

    def test_blankline(self):
        line = '     '
        assert Parser.parse(line) == { 'blank': True }

    def test_comm(self):
        line = '// comment'
        assert Parser.parse(line) == { 'blank': True }

    def test_addr(self):
        line = '@123'
        assert Parser.parse(line) == { 'addr': '123' }

    def test_addr_comm(self):
        line = '@123 // comment'
        assert Parser.parse(line) == { 'addr': '123' }

    def test_addr_symbol(self):
        line = '@sys.init'
        assert Parser.parse(line) == { 'addr': 'sys.init' }

    def test_label_symbol(self):
        line = '(sys.init)'
        assert Parser.parse(line) == { 'label': 'sys.init' }

    def test_comp(self):
        line = 'A'
        assert Parser.parse(line) == { 'comp': 'A', 'dest': None, 'jump': None }
        line = '-1'
        assert Parser.parse(line) == { 'comp': '-1', 'dest': None, 'jump': None }
        line = 'D|M'
        assert Parser.parse(line) == { 'comp': 'D|M', 'dest': None, 'jump': None }

    def test_dest_comp(self):
        line = 'D=A'
        assert Parser.parse(line) == { 'comp': 'A', 'dest': 'D', 'jump': None }
        line = 'M=0'
        assert Parser.parse(line) == { 'comp': '0', 'dest': 'M', 'jump': None }
        line = 'A=D&M'
        assert Parser.parse(line) == { 'comp': 'D&M', 'dest': 'A', 'jump': None }

    def test_comp_jump(self):
        line = 'M;JMP'
        assert Parser.parse(line) == { 'comp': 'M', 'dest': None, 'jump': 'JMP' }
        line = '1;JEQ'
        assert Parser.parse(line) == { 'comp': '1', 'dest': None, 'jump': 'JEQ' }
        line = 'D+M;JLT'
        assert Parser.parse(line) == { 'comp': 'D+M', 'dest': None, 'jump': 'JLT' }

    def test_dest_comp_jump(self):
        line = 'AM=D;JGT'
        assert Parser.parse(line) == { 'comp': 'D', 'dest': 'AM', 'jump': 'JGT' }
        line = 'MD=-1;JNE'
        assert Parser.parse(line) == { 'comp': '-1', 'dest': 'MD', 'jump': 'JNE' }
        line = 'AMD=A|D;JGE'
        assert Parser.parse(line) == { 'comp': 'A|D', 'dest': 'AMD', 'jump': 'JGE' }

    def test_dest_comp_jump_comm(self):
        line = 'AMD=A|D;JGE // comment'
        assert Parser.parse(line) == { 'comp': 'A|D', 'dest': 'AMD', 'jump': 'JGE' }

    def test_dest_comp_jump_wsp(self):
        line = 'A MD  =A   |D    ;J     GE'
        assert Parser.parse(line) == { 'comp': 'A|D', 'dest': 'AMD', 'jump': 'JGE' }

    def test_wrong_order(self):
        line = 'D+A D =; JMP'
        assert not Parser.parse(line)
