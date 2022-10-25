from token_schema import TokenSchema

class TypeValuesTokenSchema(TokenSchema):

    def __init__(self, type, values):
        self.type = type
        self.values = values

    def matches(self, token):
        return self.type == token.type and token.value in self.values

    def args(self):
        return [ self.type, self.value ]

    def in_words(self):
        values_string = '|'.join(self.values)
        return f"<{self.type} '({values_string})'>"
