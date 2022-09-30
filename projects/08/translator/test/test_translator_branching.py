import pytest

from translator import Translator

class TestTranslatorBranching:
    translator = Translator()

    def test_label(self):
        tokens = {
            'command': 'label',
            'arg1': 'FOO',
            'arg2': None
        }
        expected = "(FOO)\n"
        assembly = self.translator.translate(tokens)
        assert expected == assembly

    def test_if_goto(self):
        tokens = {
            'command': 'if-goto',
            'arg1': 'FOO',
            'arg2': None
        }
        expected = (
            # sp--
            '@SP\n'
            'M=M-1\n'
            # D = *sp
            '@SP\n'
            'A=M\n'
            'D=M\n'
            # if D != 0: goto FOO
            '@FOO\n'
            'D;JNE\n'
        )
        assembly = self.translator.translate(tokens)
        assert expected == assembly

    def test_goto(self):
        tokens = {
            'command': 'goto',
            'arg1': 'FOO',
            'arg2': None
        }
        expected = (
            "@FOO\n"
            "0;JMP\n"
        )
        assembly = self.translator.translate(tokens)
        assert expected == assembly

