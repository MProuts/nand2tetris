from token_schema import TokenSchema

class TypeTokenSchema(TokenSchema):

    def __init__(self, type):
        self.type = type

    def matches(self, token):
        return self.type == token.type

    def args(self):
        return [ self.type, '*' ]

    def in_words(self):
        return f"<{self.type}>"
