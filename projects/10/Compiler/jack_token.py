from dict2xml import dict2xml

class JackToken:

    def __init__(self, type, value):
        self.type = type
        self.value = value

    # entity encoding is not necessary for python dictionaries
    def to_dict(self):
        return { "type": self.type, "value": self.value }

    # entity encoding is necessary for xml -- dict2xml handles
    # this automatically
    def to_xml(self):
        return dict2xml({ self.type: f" {self.value} " })
