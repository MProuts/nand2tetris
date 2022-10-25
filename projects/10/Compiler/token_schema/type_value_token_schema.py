from token_schema import TokenSchema
class TypeValueTokenSchema(TokenSchema):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def matches(self, token):
        return self.type == token.type and self.value == token.value

    def args(self):
        return [ self.type, self.value ]

    def in_words(self):
        return f"<{self.type} '{self.value}'>"
