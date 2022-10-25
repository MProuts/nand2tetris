from dict2xml import dict2xml
import xmltodict

class JackToken:

    @classmethod
    def from_xml(self, io):
        items = xmltodict.parse(io).items()
        args = list(list(items)[0])
        return JackToken(*args)

    def __init__(self, type, value):
        self.type = type
        self.value = value

    # entity encoding is not necessary for python dictionaries
    def to_dict(self):
        return { "type": self.type, "value": self.value }

    # this is necessary for compatibility with the dict2xml library
    def to_xml_dict(self):
        return { self.type: self._xml_value() }

    # entity encoding is necessary for xml -- dict2xml handles
    # this automatically
    def to_xml(self):
        return dict2xml({ self.type: self._xml_value() })

    def _xml_value(self):
        return f" {self.value} "

    def to_arr(self):
        return [ self.type, self.value ]

    def in_words(self):
        return f"<{self.type} '{self.value}'>"

    def matches(self, schema):
        return self.factory.create(schema).matches(self)

    def assert_matches(self, schema):
        return self.factory.create(schema).assert_matches(self)

    def __str__(self):
        return f"<{self.type} '{self.value}'>"

    def __repr__(self):
        return f"JackToken('{self.type}','{self.value}')"

    def __eq__(self, other):
        return (self.type == other.type and self.value == other.value)
