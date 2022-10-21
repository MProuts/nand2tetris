import pytest
import io
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
            output = JackTokenizer(io)._tokens_as_xml()
            assert output.strip() == expected.strip()
