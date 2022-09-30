import pytest
import path_helper

from translator import Translator

class TestTranslator:
    translator = Translator()

    def test_add(self):
        tokens = {
            'command': 'add'
        }
        expected = (
            # sp--
            "@SP\n"
            "M=M-1\n"
            # D = *sp
            "A=M\n"
            "D=M\n"
            # sp--
            "@SP\n"
            "M=M-1\n"
            # *sp += D
            "A=M\n"
            "M=M+D\n"
            # sp++
            "@SP\n"
            "M=M+1\n"
        )
        assembly = self.translator.translate(tokens)
        assert assembly == expected

    def test_sub(self):
        tokens = {
            'command': 'sub'
        }
        expected = (
            "@SP\n"
            "M=M-1\n"
            "A=M\n"
            "D=M\n"
            "@SP\n"
            "M=M-1\n"
            # *sp -= D
            "A=M\n"
            "M=M-D\n"
            "@SP\n"
            "M=M+1\n"
        )
        assembly = self.translator.translate(tokens)
        assert assembly == expected

    def test_and(self):
        tokens = {
            'command': 'and'
        }
        expected = (
            "@SP\n"
            "M=M-1\n"
            "A=M\n"
            "D=M\n"
            "@SP\n"
            "M=M-1\n"
            # *sp &= D
            "A=M\n"
            "M=M&D\n"
            "@SP\n"
            "M=M+1\n"
        )
        assembly = self.translator.translate(tokens)
        assert assembly == expected

    def test_or(self):
        tokens = {
            'command': 'or'
        }
        expected = (
            "@SP\n"
            "M=M-1\n"
            "A=M\n"
            "D=M\n"
            "@SP\n"
            "M=M-1\n"
            # *sp |= D
            "A=M\n"
            "M=M|D\n"
            "@SP\n"
            "M=M+1\n"
        )
        assembly = self.translator.translate(tokens)
        assert assembly == expected

    def test_neg(self):
        tokens = {
            'command': 'neg'
        }
        expected = (
            # sp--
            "@SP\n"
            "M=M-1\n"
            # *sp = -*sp
            "A=M\n"
            "M=-M\n"
            # sp++
            "@SP\n"
            "M=M+1\n"
        )
        assembly = self.translator.translate(tokens)
        assert assembly == expected

    def test_eq(self):
        tokens = {
            'command': 'eq'
        }
        expected = (
            # sp--
            "@SP\n"
            "M=M-1\n"
            # D = *sp
            "A=M\n"
            "D=M\n"
            # sp--
            "@SP\n"
            "M=M-1\n"
            # setup condition
            "A=M\n"
            "D=M-D\n"
            "@TRUE47\n"
            "D;JEQ\n"
            # if D != *sp
            #   *sp = 0
            "@SP\n"
            "A=M\n"
            "M=0\n"
            "@END47\n"
            "0;JMP\n"
            # if D == *sp
            #   *sp = 1
            "(TRUE47)\n"
            "@SP\n"
            "A=M\n"
            "M=-1\n"
            "@END47\n"
            "0;JMP\n"
            # *sp++
            "(END47)\n"
            "@SP\n"
            "M=M+1\n"
        )
        assembly = self.translator.translate(tokens, 47)
        assert assembly == expected
