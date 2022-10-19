import pytest
import io
import dict2xml
import re
from pathlib import Path

from jack_tokenizer import JackTokenizer

class TestJackTokenizerFiles:
    chapter_dir = Path(__file__).parent.parent.parent

    def test_array_main(self):
        input_path = self.chapter_dir / "ArrayTest/Main.jack"
        self._test_jack_file(input_path)

    def test_square_no_e_main(self):
        input_path = self.chapter_dir / "ExpressionLessSquare/Main.jack"
        self._test_jack_file(input_path)

    def test_square_no_e_square(self):
        input_path = self.chapter_dir / "ExpressionLessSquare/Square.jack"
        self._test_jack_file(input_path)

    def test_square_no_e_square_game(self):
        input_path = self.chapter_dir / "ExpressionLessSquare/SquareGame.jack"
        self._test_jack_file(input_path)

    def test_square_main(self):
        input_path = self.chapter_dir / "Square/Main.jack"
        self._test_jack_file(input_path)

    def test_square_square(self):
        input_path = self.chapter_dir / "Square/Square.jack"
        self._test_jack_file(input_path)

    def test_square_square_game(self):
        input_path = self.chapter_dir / "Square/SquareGame.jack"
        self._test_jack_file(input_path)

    def _test_jack_file(self, input_path):
        compare_path = Path(
            input_path.parent,
            input_path.stem + 'T.xml').resolve()
        expected = open(compare_path).read()

        with open(input_path) as io:
            output = self._tokens_to_xml(JackTokenizer(io).token_gen())
            assert output.strip() == expected.strip()


    def _tokens_to_xml(self, tokens):
        formatted_tokens = []
        for token in tokens:
            new_token = {}
            type = token["type"]
            if type == "integer_constant":
                type = "integerConstant"
            if type == "string_constant":
                type = "stringConstant"

            new_token[type] = f" {token['value']} "
            formatted_tokens.append(new_token)

        converter = dict2xml.Converter(wrap="tokens", indent="")
        xml = converter.build(formatted_tokens, iterables_repeat_wrap=False)

        # dict2xml replaces '&' with '&amp;' leading to these 'double-encoded'
        # entities
        double_encodings = {
            '&amp;lt;': '&lt;',
            '&amp;gt;': '&gt;',
            '&amp;quot;': '&quot;',
            '&amp;amp;': '&amp;',
        }

        for wrong, right in double_encodings.items():
            xml = xml.replace(wrong, right)

        return xml
