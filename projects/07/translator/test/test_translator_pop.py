import pytest

from translator import Translator

class TestTranslatorPop:
    def test_pop(self):
        tokens = {
            'command': 'pop',
            'arg1': 'argument',
            'arg2': '2'
        }
        expected = (
            # sp--
            "@SP\n"
            "M=M-1\n"
            # R13 = *sp
            "@SP\n"
            "A=M\n"
            "D=M\n"
            "@R13\n"
            "M=D\n"
            # R14 = argument[2]
            "@2\n"
            "D=A\n"
            "@ARG\n"
            "D=M+D\n"
            "@R14\n"
            "M=D\n"
            # *argument[2] = *sp
            "@R13\n"
            "D=M\n"
            "@R14\n"
            "A=M\n"
            "M=D\n"
        )
        assembly = Translator.translate(tokens)
        assert assembly == expected

    def test_pop_temp(self):
        tokens = {
            'command': 'pop',
            'arg1': 'temp',
            'arg2': '6'
        }
        expected = (
            # sp--
            "@SP\n"
            "M=M-1\n"
            # temp[6] = *sp
            "@SP\n"
            "A=M\n"
            "D=M\n"
            "@11\n"
            "M=D\n"
        )
        assembly = Translator.translate(tokens)
        assert assembly == expected

    def test_pop_pointer(self):
        tokens = {
            'command': 'pop',
            'arg1': 'pointer',
            'arg2': '1'
        }
        expected = (
            # sp--
            "@SP\n"
            "M=M-1\n"
            # pointer[1] = *sp
            "@SP\n"
            "A=M\n"
            "D=M\n"
            "@4\n"
            "M=D\n"
        )
        assembly = Translator.translate(tokens)
        assert assembly == expected

    def test_pop_static(self):
        tokens = {
            'command': 'pop',
            'arg1': 'static',
            'arg2': '1'
        }
        expected = (
            # sp--
            "@SP\n"
            "M=M-1\n"
            # static[1] = *sp
            "@SP\n"
            "A=M\n"
            "D=M\n"
            "@foo.1\n"
            "M=D\n"
        )
        assembly = Translator.translate(tokens, source_name='foo')
        assert assembly == expected
