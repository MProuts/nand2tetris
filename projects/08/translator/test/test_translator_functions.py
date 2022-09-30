import pytest
from template_helper import render_test

from translator import Translator

class TestTranslatorFunctions:
    translator = Translator()

    def test_function(self):
        tokens = {
            'command': 'function',
            'arg1': 'Foo.bar',
            'arg2': '2'
        }
        expected = (
            "(Foo.bar)\n"
            # push 0
            "@0\n"
            "D=A\n"
            "@SP\n"
            "A=M\n"
            "M=D\n"
            "@SP\n"
            "M=M+1\n"
            # push 0
            "@0\n"
            "D=A\n"
            "@SP\n"
            "A=M\n"
            "M=D\n"
            "@SP\n"
            "M=M+1\n"
        )
        assembly = self.translator.translate(tokens)
        assert expected == assembly

    def test_return(self):
        tokens = {
            'command': 'return',
            'arg1': None,
            'arg2': None,
        }
        expected = render_test('return')
        assembly = self.translator.translate(tokens)
        assert expected == assembly


    def test_call(self):
        translator = Translator(return_index=47)
        tokens = {
            'command': 'call',
            'arg1': 'Foo.bar',
            'arg2': '2'
        }
        expected = render_test('call')
        assembly = translator.translate(tokens)
        assert expected == assembly
        assert translator.return_index == 48
