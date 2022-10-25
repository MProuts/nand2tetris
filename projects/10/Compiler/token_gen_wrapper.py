class TokenGenWrapper:

    def __init__(self, token_gen, initial_current=False):
        self.token_gen = token_gen
        if initial_current:
            self.__next__()
        else:
            self.current = None

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.current = next(self.token_gen)
        except StopIteration:
            self.current = None
        return self.current
