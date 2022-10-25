import pytest

import path_helper
from jack_token import JackToken
from jack_parser import JackParser
from test_helper import assert_xml_equal

class TestJackParserProgramStructure:

    def test_empty_class(self):
        tokens = [
            ['keyword', 'class'],
            ['identifier', 'FooBar'],
            ['symbol', '{'],
            ['symbol', '}'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_class()

        expected = """
            <class>
                <keyword> class </keyword>
                <identifier> FooBar </identifier>
                <symbol> { </symbol>
                <symbol> } </symbol>
            </class>
        """
        assert_xml_equal(parser._read(), expected)

    def test_class_var_dec(self):
        tokens = [
            ['keyword', 'static'],
            ['identifier', 'SquareGame'],
            ['identifier', 'game'],
            ['symbol', ';'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_class_var_dec()

        expected = """
            <classVarDec>
              <keyword> static </keyword>
              <identifier> SquareGame </identifier>
              <identifier> game </identifier>
              <symbol> ; </symbol>
            </classVarDec>
        """
        assert_xml_equal(parser._read(), expected)

    def test_class_var_dec_multiple(self):
        tokens = [
            ['keyword', 'field'],
            ['keyword', 'int'],
            ['identifier', 'foo'],
            ['symbol', ','],
            ['identifier', 'bar'],
            ['symbol', ','],
            ['identifier', 'baz'],
            ['symbol', ';'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_class_var_dec()

        expected = """
            <classVarDec>
              <keyword> field </keyword>
              <keyword> int </keyword>
              <identifier> foo </identifier>
              <symbol> , </symbol>
              <identifier> bar </identifier>
              <symbol> , </symbol>
              <identifier> baz </identifier>
              <symbol> ; </symbol>
            </classVarDec>
        """
        assert_xml_equal(parser._read(), expected)

    def test_class_var_dec_multiple_invalid(self):
        tokens = [
            ['keyword', 'field'],
            ['keyword', 'int'],
            ['identifier', 'foo'],
            ['symbol', ','],
            ['identifier', 'bar'],
            ['symbol', ','],
            ['identifier', 'baz'],
            ['symbol', '+'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)

        with pytest.raises(ValueError):
            parser.compile_class_var_dec()

    def test_subroutine_dec(self):
        tokens = [
            ['keyword', 'constructor'],
            ['identifier', 'FooBar'],
            ['identifier', 'foo'],
            ['symbol', '('],
            ['keyword', 'int'],
            ['identifier', 'foo'],
            ['symbol', ')'],
            ['symbol', '{'],
            ['symbol', '}'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_subroutine_dec()

        expected = """
            <subroutineDec>
                <keyword> constructor </keyword>
                <identifier> FooBar </identifier>
                <identifier> foo </identifier>
                <symbol> ( </symbol>
                <parameterList>
                    <keyword> int </keyword>
                    <identifier> foo </identifier>
                </parameterList>
                <symbol> ) </symbol>
                <subroutineBody>
                    <symbol> { </symbol>
                    <statements>
                    </statements>
                    <symbol> } </symbol>
                </subroutineBody>
            </subroutineDec>
        """
        assert_xml_equal(parser._read(), expected)

    def test_parameter_list_empty(self):
        tokens = [
            ['symbol', ')'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_parameter_list()

        expected = """
            <parameterList>
            </parameterList>
        """
        assert_xml_equal(parser._read(), expected)

    def test_parameter_list_single(self):
        tokens = [
            ['keyword', 'int'],
            ['identifier', 'foo'],
            ['symbol', ')'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_parameter_list()

        expected = """
            <parameterList>
                <keyword> int </keyword>
                <identifier> foo </identifier>
            </parameterList>
        """
        assert_xml_equal(parser._read(), expected)

    def test_parameter_list_multiple(self):
        tokens = [
            ['keyword', 'int'],
            ['identifier', 'foo'],
            ['symbol', ','],
            ['identifier', 'FooBar'],
            ['identifier', 'bar'],
            ['symbol', ')'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_parameter_list()

        expected = """
            <parameterList>
                <keyword> int </keyword>
                <identifier> foo </identifier>
                <symbol> , </symbol>
                <identifier> FooBar </identifier>
                <identifier> bar </identifier>
            </parameterList>
        """
        assert_xml_equal(parser._read(), expected)

    def test_subroutine_body(self):
        tokens = [
            ['symbol', '{'],
            ['symbol', '}'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_subroutine_body()

        expected = """
            <subroutineBody>
                <symbol> { </symbol>
                <statements>
                </statements>
                <symbol> } </symbol>
            </subroutineBody>
        """
        assert_xml_equal(parser._read(), expected)

    def test_empty_var_dec(self):
        tokens = [
            # end of var dec
            ['keyword', 'do'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_var_dec()

        expected = """
            <varDec>
            </varDec>
        """
        assert_xml_equal(parser._read(), expected)

    def test_var_dec(self):
        tokens = [
            ['keyword', 'var'],
            ['identifier', 'SquareGame'],
            ['identifier', 'game'],
            ['symbol', ';'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_var_dec()

        expected = """
            <varDec>
              <keyword> var </keyword>
              <identifier> SquareGame </identifier>
              <identifier> game </identifier>
              <symbol> ; </symbol>
            </varDec>
        """
        assert_xml_equal(parser._read(), expected)

    def test_var_dec_multiple(self):
        tokens = [
            ['keyword', 'var'],
            ['keyword', 'int'],
            ['identifier', 'foo'],
            ['symbol', ','],
            ['identifier', 'bar'],
            ['symbol', ','],
            ['identifier', 'baz'],
            ['symbol', ';'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_var_dec()

        expected = """
            <varDec>
              <keyword> var </keyword>
              <keyword> int </keyword>
              <identifier> foo </identifier>
              <symbol> , </symbol>
              <identifier> bar </identifier>
              <symbol> , </symbol>
              <identifier> baz </identifier>
              <symbol> ; </symbol>
            </varDec>
        """
        assert_xml_equal(parser._read(), expected)

    def test_var_dec_multiple_invalid(self):
        tokens = [
            ['keyword', 'var'],
            ['keyword', 'int'],
            ['identifier', 'foo'],
            ['symbol', ','],
            ['identifier', 'bar'],
            ['symbol', ','],
            ['identifier', 'baz'],
            ['symbol', '+'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)

        with pytest.raises(ValueError):
            parser.compile_var_dec()
