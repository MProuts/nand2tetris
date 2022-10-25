import pytest

import path_helper
from jack_token import JackToken
from jack_parser import JackParser
from test_helper import assert_xml_equal

class TestJackParserStatements:

    def test_empty_statements(self):
        tokens = []
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_statements()

        expected = """
            <statements>
            </statements>
        """
        assert_xml_equal(parser._read(), expected)

    def test_let(self):
        tokens = [
            ['keyword', 'let'],
            ['identifier', 'bar'],
            ['symbol', '='],
            ['identifier', 'bar'],
            ['symbol', '+'],
            ['integerConstant', '1'],
            ['symbol', ';'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_statements()

        expected = """
            <statements>
                <letStatement>
                    <keyword> let </keyword>
                    <identifier> bar </identifier>
                    <symbol> = </symbol>
                    <expression>
                        <term>
                            <identifier> bar </identifier>
                        </term>
                        <symbol> + </symbol>
                        <term>
                            <integerConstant> 1 </integerConstant>
                        </term>
                    </expression>
                    <symbol> ; </symbol>
                </letStatement>
            </statements>
        """
        assert_xml_equal(parser._read(), expected)

    def test_let_brackets(self):
        tokens = [
            ['keyword', 'let'],
            ['identifier', 'bar'],
            ['symbol', '['],
            ['integerConstant', '1'],
            ['symbol', ']'],
            ['symbol', '='],
            ['symbol', '('],
            ['identifier', 'bar'],
            ['symbol', '+'],
            ['integerConstant', '1'],
            ['symbol', ')'],
            ['symbol', ';'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_statements()

        expected = """
            <statements>
                <letStatement>
                    <keyword> let </keyword>
                    <identifier> bar </identifier>
                    <symbol> [ </symbol>
                    <expression>
                        <term>
                            <integerConstant> 1 </integerConstant>
                        </term>
                    </expression>
                    <symbol> ] </symbol>
                    <symbol> = </symbol>
                    <expression>
                        <term>
                            <symbol> ( </symbol>
                            <expression>
                                <term>
                                    <identifier> bar </identifier>
                                </term>
                                <symbol> + </symbol>
                                <term>
                                    <integerConstant> 1 </integerConstant>
                                </term>
                            </expression>
                            <symbol> ) </symbol>
                        </term>
                    </expression>
                    <symbol> ; </symbol>
                </letStatement>
            </statements>
        """
        assert_xml_equal(parser._read(), expected)

    def test_if(self):
        tokens = [
            ['keyword', 'if'],
            ['symbol', '('],
            ['keyword', 'true'],
            ['symbol', ')'],
            ['symbol', '{'],
            ['symbol', '}'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_statements()

        expected = """
            <statements>
                <ifStatement>
                    <keyword> if </keyword>
                    <symbol> ( </symbol>
                    <expression>
                        <term>
                            <keyword> true </keyword>
                        </term>
                    </expression>
                    <symbol> ) </symbol>
                    <symbol> { </symbol>
                        <statements>
                        </statements>
                    <symbol> } </symbol>
                </ifStatement>
            </statements>
        """
        assert_xml_equal(parser._read(), expected)

    def test_if_else(self):
        tokens = [
            ['keyword', 'if'],
            ['symbol', '('],
            ['keyword', 'true'],
            ['symbol', ')'],
            ['symbol', '{'],
            ['symbol', '}'],
            ['keyword', 'else'],
            ['symbol', '{'],
            ['symbol', '}'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_statements()

        expected = """
            <statements>
                <ifStatement>
                    <keyword> if </keyword>
                    <symbol> ( </symbol>
                    <expression>
                        <term>
                            <keyword> true </keyword>
                        </term>
                    </expression>
                    <symbol> ) </symbol>
                    <symbol> { </symbol>
                        <statements>
                        </statements>
                    <symbol> } </symbol>
                    <keyword> else </keyword>
                    <symbol> { </symbol>
                        <statements>
                        </statements>
                    <symbol> } </symbol>
                </ifStatement>
            </statements>
        """
        assert_xml_equal(parser._read(), expected)

    def test_while(self):
        tokens = [
            ['keyword', 'while'],
            ['symbol', '('],
            ['keyword', 'true'],
            ['symbol', ')'],
            ['symbol', '{'],
            ['symbol', '}'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_statements()

        expected = """
            <statements>
                <whileStatement>
                    <keyword> while </keyword>
                    <symbol> ( </symbol>
                    <expression>
                        <term>
                            <keyword> true </keyword>
                        </term>
                    </expression>
                    <symbol> ) </symbol>
                    <symbol> { </symbol>
                        <statements>
                        </statements>
                    <symbol> } </symbol>
                </whileStatement>
            </statements>
        """
        assert_xml_equal(parser._read(), expected)

    def test_do_function_call(self):
        tokens = [
            ['keyword', 'do'],
            ['identifier', 'foo'],
            ['symbol', '('],
            ['identifier', 'foo'],
            ['symbol', ')'],
            ['symbol', ';'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_statements()

        expected = """
            <statements>
                <doStatement>
                    <keyword> do </keyword>
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
                    <symbol> ; </symbol>
                </doStatement>
            </statements>
        """
        assert_xml_equal(parser._read(), expected)

    def test_empty_return(self):
        tokens = [
            ['keyword', 'return'],
            ['symbol', ';'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_statements()

        expected = """
            <statements>
                <returnStatement>
                    <keyword> return </keyword>
                    <symbol> ; </symbol>
                </returnStatement>
            </statements>
        """
        assert_xml_equal(parser._read(), expected)

    def test_return_expression(self):
        tokens = [
            ['keyword', 'return'],
            ['identifier', 'foo'],
            ['symbol', '['],
            ['identifier', 'foo'],
            ['symbol', ']'],
            ['symbol', ';'],
        ]
        token_gen = (JackToken(*token) for token in tokens)
        parser = JackParser(token_gen)
        parser.compile_statements()

        expected = """
            <statements>
                <returnStatement>
                    <keyword> return </keyword>
                    <expression>
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
                    </expression>
                    <symbol> ; </symbol>
                </returnStatement>
            </statements>
        """
        assert_xml_equal(parser._read(), expected)

