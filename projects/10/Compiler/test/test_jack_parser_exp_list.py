import pytest

import path_helper
from jack_token import JackToken
from jack_parser import JackParser
from test_helper import assert_xml_equal

class TestJackParserExpList:

    def test_empty_expression_list(self):
        tokens = [
            ['symbol', ')'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_expression_list()
        expected = """
            <expressionList>
            </expressionList>
        """
        assert_xml_equal(parser._read(), expected)

    def test_single_expression_list(self):
        tokens = [
            ['keyword', 'false'],
            ['symbol', '&'],
            ['keyword', 'false'],
            ['symbol', ')'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_expression_list()
        expected = """
            <expressionList>
                <expression>
                    <term>
                      <keyword> false </keyword>
                    </term>
                    <symbol> &amp; </symbol>
                    <term>
                      <keyword> false </keyword>
                    </term>
                </expression>
            </expressionList>
        """
        assert_xml_equal(parser._read(), expected)

    def test_multiple_expression_list(self):
        tokens = [
            # expression 1
            ['keyword', 'false'],
            ['symbol', '&'],
            ['keyword', 'false'],

            ['symbol', ','],

            # expression 2
            ['identifier', 'foo'],
            ['symbol', '('],
            ['identifier', 'foo'],
            ['symbol', ')'],

            ['symbol', '-'],

            ['identifier', 'bar'],
            ['symbol', '['],
            ['identifier', 'bar'],
            ['symbol', ']'],

            # end of list
            ['symbol', ')'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_expression_list()
        expected = """
            <expressionList>
                <expression>
                    <term>
                      <keyword> false </keyword>
                    </term>
                    <symbol> &amp; </symbol>
                    <term>
                      <keyword> false </keyword>
                    </term>
                </expression>
                <symbol> , </symbol>
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
            </expressionList>
        """
        assert_xml_equal(parser._read(), expected)
