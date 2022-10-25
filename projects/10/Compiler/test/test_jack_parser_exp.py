import pytest

import path_helper
from jack_token import JackToken
from jack_parser import JackParser
from test_helper import assert_xml_equal

class TestJackParserExp:

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

