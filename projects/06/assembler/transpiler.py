class Transpiler:
    comp_to_bin = {
        '0':   '0101010', '1':   '0111111', '-1':  '0111010',
        'D':   '0001100', 'A':   '0110000', 'M':   '1110000',
        '!D':  '0001101', '!A':  '0110001', '!M':  '1110001',
        '-D':  '0001111', '-A':  '0110011', '-M':  '1110011',
        'D+1': '0011111', 'A+1': '0110111', 'M+1': '1110111',
        'D-1': '0001110', 'A-1': '0110010', 'M-1': '1110010',
        'D+A': '0000010', 'D+M': '1000010', 'D-A': '0010011',
        'D-M': '1010011', 'A-D': '0000111', 'M-D': '1000111',
        'D&A': '0000000', 'D&M': '1000000',
        'D|A': '0010101', 'D|M': '1010101'
    }

    dest_to_bin = {
        None:  '000',
        'M':   '001',
        'D':   '010',
        'MD':  '011',
        'A':   '100',
        'AM':  '101',
        'AD':  '110',
        'AMD': '111'
    }

    jump_to_bin = {
        None:  '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }

    @classmethod
    def validate(self, tokens, symbol_table):
        if 'blank' in tokens:
            raise ValueError("Transpiler received blank line")

        if not 'addr' in tokens and not 'comp' in tokens:
            raise ValueError("Invalid inst: addr, comp, or label must be present")

        if 'comp' in tokens:
            if not tokens['comp'] in self.comp_to_bin:
                raise ValueError(f"Invalid comp: {tokens['comp']}")

        if 'dest' in tokens:
            if not tokens['dest'] in self.dest_to_bin:
                raise ValueError(f"Invalid dest: {tokens['dest']}")

        if 'jump' in tokens:
            if not tokens['jump'] in self.jump_to_bin:
                    raise ValueError(f"Invalid jump: {tokens['jump']}")

    @classmethod
    def transpile(self, tokens, symbol_table):
        if 'addr' in tokens:
            if not tokens['addr'].isnumeric():
                addr_int = symbol_table.get(tokens['addr'])
            else:
                addr_int = int(tokens['addr'])

            addr_bin = '{:016b}'.format(addr_int)
            return addr_bin

        else:
            comp_bin = self.comp_to_bin[tokens['comp']]
            dest_bin = self.dest_to_bin[tokens['dest']]
            jump_bin = self.jump_to_bin[tokens['jump']]
            return f'111{comp_bin}{dest_bin}{jump_bin}'
