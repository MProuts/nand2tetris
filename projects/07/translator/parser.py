import re

class Parser:
    # Regex to match command components
    pattern_str = r'^\s*(?P<command>\S+)( (?P<arg1>\S+)( (?P<arg2>\S+)\s*)?)?$'

    @classmethod
    def parse(self, line):
        # Remove comments
        line = re.sub(r'//.*', '', line)

        # Ignore empty lines
        if len(line) == 0 or line.isspace():
            return { 'blank': True }

        # Remove extra whitespace
        line = line.strip()
        line = re.sub(r'\s{2,}', ' ', line)

        match = re.match(self.pattern_str, line)

        if not match:
            return {}

        return match.groupdict()
