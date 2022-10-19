import re

class JackTokenizer:
    KEYWORDS = [
        'class',
        'constructor', 'function', 'method',
        'field', 'static', 'var',
        'int', 'char', 'boolean', 'void',
        'true', 'false', 'null', 'this',
        'let', 'do', 'if', 'else', 'while',
        'return',
    ]

    SYMBOLS = [
        '{', '}', '(', ')', '[', ']',
        '.', ',', ';',
        '+', '-', '*', '/',
        '&', '|', '~',
        '<', '>', '=',
    ]

    SYMBOL_ENCODING = {
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        '&': '&amp;',
    }

    PATTERN_WHITESPACE = re.compile(r'\s')
    PATTERN_DIGIT = re.compile(r'\d')
    PATTERN_WORD_START = re.compile(r'[a-zA-Z_]')
    PATTERN_WORD_CHAR = re.compile(r'\w')

    def __init__(self, io):
        self.io = io

    def token_gen(self):
        current_char = self.io.read(1)
        current_string = ""
        while current_char:

            # comments
            # ========
            if current_char == '/':
                current_pair = current_char + self.io.read(1)
                if current_pair == '//':
                    while current_char != '\n':
                        current_char = self.io.read(1)
                    # prepare for next iteration
                    current_char = self.io.read(1)
                    continue
                elif current_pair == '/*':
                    while not current_pair == '*/':
                        current_pair = current_pair[1:] + self.io.read(1)
                    # prepare for next iteration
                    current_char = self.io.read(1)
                    continue
                else:
                    self._rewind(1)
                    # Don't continue here -- if '/' is not part of a comment, it
                    # should be treated as a symbol, which is handled below.

            # whitespace
            # ==========
            if self._is_whitespace(current_char):
                current_char = self.io.read(1)
                continue

            # symbols
            # =======
            if self._is_symbol(current_char):
                value = self._encode_symbol(current_char)
                yield { "type": "symbol", "value": value }
                current_char = self.io.read(1)
                continue

            # integer constants
            # =================
            if self._is_digit(current_char):
                current_string = ""
                while self._is_digit(current_char):
                    current_string += current_char
                    current_char = self.io.read(1)

                if int(current_string) > 32767:
                    msg = "Integer constants must be between 0 and 32767"
                    raise ValueError(msg)

                yield { "type": "integer_constant", "value": current_string }
                continue

            # string constants
            # ================
            if current_char == '"':
                current_string = ""
                # Ignore opening quote
                current_char = self.io.read(1)
                while not current_char == '"':
                    current_string += current_char
                    current_char = self.io.read(1)

                # Ignore closing quote
                current_char = self.io.read(1)
                yield { "type": "string_constant", "value": current_string }
                continue

            # keyword or identifier
            # =====================
            if self._is_word_start(current_char):
                current_string = ""

                # This loop terminates when we reach a non-letter. Note
                # that we don't increment current_char before continuing. That way the
                # non-letter character gets handled appropriately in the outer
                # loop.
                while self._is_word_char(current_char):
                    current_string += current_char
                    current_char = self.io.read(1)

                if current_string in self.KEYWORDS:
                    yield { "type": "keyword", "value": current_string }
                else:
                    yield { "type": "identifier", "value": current_string }
                continue

            # error
            # =====
            # We should never get here -- each if clause above is responsible
            # for incrementing current_char and continuing to the next iteration
            # as needed
            raise ValueError(f"Invalid character '{current_char}'")

        # end while
        # =========
        # reset to beginning of stream
        self.io.seek(0)

    # private methods
    # ===============
    def _rewind(self, n):
        self.io.seek(self.io.tell() - n)

    def _is_whitespace(self, char):
        return self.PATTERN_WHITESPACE.match(char)

    def _is_symbol(self, char):
        return char in self.SYMBOLS

    def _encode_symbol(self, char):
        if char in self.SYMBOL_ENCODING:
            return self.SYMBOL_ENCODING[char]
        else:
            return char

    def _is_word_start(self, char):
        return self.PATTERN_WORD_START.match(char)

    def _is_word_char(self, char):
        return self.PATTERN_WORD_CHAR.match(char)

    def _is_digit(self, char):
        return self.PATTERN_DIGIT.match(char)

    # convenience methods
    # ===================
    # ! This will load everything into memory -- for testing only
    def _tokens(self):
        return [token for token in self.token_gen()]
