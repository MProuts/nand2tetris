import copy

class SymbolTable:
    PREDEFINED_SYMBOLS = {
        'SP':     0,
        'LCL':    1,
        'ARG':    2,
        'THIS':   3,
        'THAT':   4,
        'R0':     0,
        'R1':     1,
        'R2':     2,
        'R3':     3,
        'R4':     4,
        'R5':     5,
        'R6':     6,
        'R7':     7,
        'R8':     8,
        'R9':     9,
        'R10':    10,
        'R11':    11,
        'R12':    12,
        'R13':    13,
        'R14':    14,
        'R15':    15,
        'SCREEN': 16384,
        'KBD':    24576,
    }

    def __init__(self):
        self._table = copy.deepcopy(self.PREDEFINED_SYMBOLS)
        self.n = 16

    def set(self, key, value):
        self._table[key] = value

    def get(self, key):
        if key in self._table:
            return self._table[key]
        else:
            n_temp = self.n
            self._table[key] = n_temp
            self.n += 1
            return n_temp

    def _defined_symbols(self):
        defined_keys = set(self._table) - set(self.PREDEFINED_SYMBOLS)
        return { k : self._table[k] for k in defined_keys }
