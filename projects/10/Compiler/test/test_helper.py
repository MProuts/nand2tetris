from pathlib import Path
from path_helper import root_path

def assert_xml_equal(first, other):
    first = _lstrip_lines(first).strip()
    other = _lstrip_lines(other).strip()
    assert first == other

def _lstrip_lines(string):
    fn = lambda line: line.lstrip()
    mapped = map(fn, string.split('\n'))
    return '\n'.join(mapped)
