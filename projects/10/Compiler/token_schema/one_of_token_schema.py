from token_schema import TokenSchema

class OneOfTokenSchema(TokenSchema):

    def __init__(self, expect1, expect2):
        self.expect1 = expect1
        self.expect2 = expect2

    def matches(self, token):
        satisfied_1 = self.expect1.matches(token)
        satisfied_2 = self.expect2.matches(token)
        return (satisfied_1 or satisfied_2)

    def args(self):
        args1 = self.expect1.args()
        args2 = self.expect2.args()
        return { 'one_of': [ args1, args2 ] }

    def in_words(self):
        in_words1 = self.expect1.in_words()
        in_words2 = self.expect2.in_words()
        return f"{in_words1} or {in_words2}"
