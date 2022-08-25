import re
from typing import Optional

class Parser:
    # Regex to match A-instructions
    a_pattern_str = r'@(?P<addr>\S+)'
    # Regex to match C-instructions
    c_pattern_str = r'^(?:(?P<dest>\w+)=)?(?P<comp>(?:\w|[!\+\-&|])+)(?:;(?P<jump>\w+))?$'
    # Regex to match label pseudo-instructions
    l_pattern_str = r'\((?P<label>\S+)\)'

    @classmethod
    def parse(self, line) -> Optional[dict]:
        # Remove comments
        pattern = re.compile(r'(?P<addr>//.*)')
        line = pattern.sub('', line)

        # Remove whitespace
        pattern = re.compile(r'\s')
        line = pattern.sub('', line)

        # Ignore empty lines
        if len(line) == 0:
            return { 'blank': True }

        # Select pattern string
        if line[0] == '@':
            pattern_str = re.compile(self.a_pattern_str)
        elif line[0] == '(':
            pattern_str = re.compile(self.l_pattern_str)
        else:
            pattern_str = re.compile(self.c_pattern_str)

        # Match pattern string
        pattern = re.compile(pattern_str)
        match = pattern.match(line)

        if not match:
            return {}

        return match.groupdict()
