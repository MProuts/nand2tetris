import pytest

import path_helper
from jack_token import JackToken
from jack_parser import JackParser
from test_helper import assert_xml_equal

class TestJackParserTerm:

    def test_expression_const(self):
        tokens = [
            ['integerConstant', '1'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)

        parser.compile_expression()
        expected = """
            <expression>
                <term>
                  <integerConstant> 1 </integerConstant>
                </term>
            </expression>
        """
        assert_xml_equal(parser._read(), expected)

    def test_expression_boolean(self):
        tokens = [
            ['keyword', 'false'],
            ['symbol', '&'],
            ['keyword', 'false'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_expression()
        expected = """
            <expression>
                <term>
                  <keyword> false </keyword>
                </term>
                <symbol> &amp; </symbol>
                <term>
                  <keyword> false </keyword>
                </term>
            </expression>
        """
        assert_xml_equal(parser._read(), expected)

    def test_expression_subroutine_indexing(self):
        tokens = [
            ['identifier', 'foo'],
            ['symbol', '('],
            ['identifier', 'foo'],
            ['symbol', ')'],

            ['symbol', '-'],

            ['identifier', 'bar'],
            ['symbol', '['],
            ['identifier', 'bar'],
            ['symbol', ']']
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_expression()
        expected = """
            <expression>
                <term>
                    <identifier> foo </identifier>
                    <symbol> ( </symbol>
                    <expressionList>
                        <expression>
                            <term>
                                <identifier> foo </identifier>
                            </term>
                        </expression>
                    </expressionList>
                    <symbol> ) </symbol>
                </term>
                <symbol> - </symbol>
                <term>
                    <identifier> bar </identifier>
                    <symbol> [ </symbol>
                    <expression>
                        <term>
                            <identifier> bar </identifier>
                        </term>
                    </expression>
                    <symbol> ] </symbol>
                </term>
            </expression>
        """
        assert_xml_equal(parser._read(), expected)

    def test_term_constants(self):
        tokens = [
            ['integerConstant', '1'],
            ['stringConstant', 'foo'],
            ['keyword', 'true'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)

        parser.compile_term()
        parser.compile_term()
        parser.compile_term()
        expected = """
            <term>
              <integerConstant> 1 </integerConstant>
            </term>
            <term>
              <stringConstant> foo </stringConstant>
            </term>
            <term>
                <keyword> true </keyword>
            </term>
        """
        assert_xml_equal(parser._read(), expected)

    def test_term_unary(self):
        tokens = [
            ['symbol', '-'],
            ['symbol', '~'],
            ['identifier', 'foo'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)

        parser.compile_term()
        expected = """
            <term>
                <symbol> - </symbol>
                <term>
                    <symbol> ~ </symbol>
                    <term>
                        <identifier> foo </identifier>
                    </term>
                </term>
            </term>
        """
        assert_xml_equal(parser._read(), expected)

    def test_term_parens(self):
        tokens = [
            JackToken('symbol', '('),
            JackToken('identifier', 'baz'),
            JackToken('symbol', '+'),
            JackToken('identifier', 'boo'),
            JackToken('symbol', '/'),
            JackToken('identifier', 'boz'),
            JackToken('symbol', ')'),
        ]
        token_gen = (token for token in tokens)
        parser = JackParser(token_gen)

        parser.compile_term()
        expected = """
            <term>
                <symbol> ( </symbol>
                <expression>
                    <term>
                        <identifier> baz </identifier>
                    </term>
                    <symbol> + </symbol>
                    <term>
                        <identifier> boo </identifier>
                    </term>
                    <symbol> / </symbol>
                    <term>
                        <identifier> boz </identifier>
                    </term>
                </expression>
                <symbol> ) </symbol>
            </term>
        """
        assert_xml_equal(parser._read(), expected)
    def test_term_variable(self):
        tokens = [
            ['identifier', 'foo'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)

        parser.compile_term()
        expected = """
            <term>
                <identifier> foo </identifier>
            </term>
        """
        assert_xml_equal(parser._read(), expected)

    def test_term_square_brackets(self):
        tokens = [
            ['identifier', 'foo'],
            ['symbol', '['],
            ['identifier', 'foo'],
            ['symbol', ']'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)

        parser.compile_term()
        expected = """
            <term>
                <identifier> foo </identifier>
                <symbol> [ </symbol>
                <expression>
                    <term>
                        <identifier> foo </identifier>
                    </term>
                </expression>
                <symbol> ] </symbol>
            </term>
        """
        assert_xml_equal(parser._read(), expected)

    def test_term_funtion_call(self):
        tokens = [
            ['identifier', 'foo'],
            ['symbol', '('],
            ['identifier', 'foo'],
            ['symbol', ')'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)

        parser.compile_term()
        expected = """
            <term>
                <identifier> foo </identifier>
                <symbol> ( </symbol>
                <expressionList>
                    <expression>
                        <term>
                            <identifier> foo </identifier>
                        </term>
                    </expression>
                </expressionList>
                <symbol> ) </symbol>
            </term>
        """
        assert_xml_equal(parser._read(), expected)

    def test_term_method_call(self):
        tokens = [
            ['identifier', 'foo'],
            ['symbol', '.'],
            ['identifier', 'foo'],
            ['symbol', '('],
            ['identifier', 'foo'],
            ['symbol', ')'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)

        parser.compile_term()
        expected = """
            <term>
                <identifier> foo </identifier>
                <symbol> . </symbol>
                <identifier> foo </identifier>
                <symbol> ( </symbol>
                <expressionList>
                    <expression>
                        <term>
                            <identifier> foo </identifier>
                        </term>
                    </expression>
                </expressionList>
                <symbol> ) </symbol>
            </term>
        """
        assert_xml_equal(parser._read(), expected)

    def test_term_method_call_exp_list(self):
        tokens = [
            ['identifier', 'foo'],
            ['symbol', '.'],
            ['identifier', 'bar'],
            ['symbol', '('],
            ['identifier', 'baz'],
            ['symbol', ','],
            ['identifier', 'boo'],
            ['symbol', ','],
            ['identifier', 'boz'],
            ['symbol', ')'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)

        parser.compile_term()
        expected = """
            <term>
                <identifier> foo </identifier>
                <symbol> . </symbol>
                <identifier> bar </identifier>
                <symbol> ( </symbol>
                <expressionList>
                    <expression>
                        <term>
                            <identifier> baz </identifier>
                        </term>
                    </expression>
                    <symbol> , </symbol>
                    <expression>
                        <term>
                            <identifier> boo </identifier>
                        </term>
                    </expression>
                    <symbol> , </symbol>
                    <expression>
                        <term>
                            <identifier> boz </identifier>
                        </term>
                    </expression>
                </expressionList>
                <symbol> ) </symbol>
            </term>
        """
        assert_xml_equal(parser._read(), expected)
