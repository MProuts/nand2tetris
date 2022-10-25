# stand for: abstract base class
from abc import ABC, abstractmethod

class TokenSchema(ABC):

    @abstractmethod
    def matches(self, token):
        raise NotImplementedError

    @abstractmethod
    def args(self):
        raise NotImplementedError

    @abstractmethod
    def in_words(self):
        raise NotImplementedError

    def assert_matches(self, token):
        if not self.matches(token):
            raise ValueError(self.error_msg(token))

    def error_msg(self, token):
        return f"Expected {self.in_words()}, got {token.in_words()}"

    def __str__(self):
        return f"<TokenSchema {self.args()}>"

    def __repr__(self):
        return f"TokenSchemaFactory.create({self.args()})"
