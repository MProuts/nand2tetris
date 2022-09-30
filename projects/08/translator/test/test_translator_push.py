import pytest

from translator import Translator

class TestTranslatorPush:
    translator = Translator()
    # .translate()
    # ===========
    def test_push_constant(self):
        tokens = {
            'command': 'push',
            'arg1': 'constant',
            'arg2': '7'
        }
        expected = (
            "@7\n"
            "D=A\n"
            "@SP\n"
            "A=M\n"
            "M=D\n"
            "@SP\n"
            "M=M+1\n"
        )
        assembly = self.translator.translate(tokens)
        assert assembly == expected

    def test_push_segment_pointer(self):
        tokens = {
            'command': 'push',
            'arg1': 'argument',
            'arg2': '2'
        }
        expected = (
            # D = *argument[2]
            "@2\n"
            "D=A\n"
            "@ARG\n"
            "A=M+D\n"
            "D=M\n"
            # *sp = D
            "@SP\n"
            "A=M\n"
            "M=D\n"
            # sp++
            "@SP\n"
            "M=M+1\n"
        )
        assembly = self.translator.translate(tokens)
        assert assembly == expected

    def test_push_temp(self):
        tokens = {
            'command': 'push',
            'arg1': 'temp',
            'arg2': '6'
        }
        expected = (
            # D = *temp[2]
            "@11\n"
            "D=M\n"
            # *sp = D
            "@SP\n"
            "A=M\n"
            "M=D\n"
            # sp++
            "@SP\n"
            "M=M+1\n"
        )
        assembly = self.translator.translate(tokens)
        assert assembly == expected

    def test_push_pointer(self):
        tokens = {
            'command': 'push',
            'arg1': 'pointer',
            'arg2': '1'
        }
        expected = (
            # D = *pointer[1]
            "@4\n"
            "D=M\n"
            # *sp = D
            "@SP\n"
            "A=M\n"
            "M=D\n"
            # sp++
            "@SP\n"
            "M=M+1\n"
        )
        assembly = self.translator.translate(tokens)
        assert assembly == expected

    def test_push_static(self):
        tokens = {
            'command': 'push',
            'arg1': 'static',
            'arg2': '1'
        }
        expected = (
            # D = *static[1]
            "@foo.1\n"
            "D=M\n"
            # *sp = D
            "@SP\n"
            "A=M\n"
            "M=D\n"
            # sp++
            "@SP\n"
            "M=M+1\n"
        )
        assembly = self.translator.translate(tokens, source_name='foo')
        assert assembly == expected
