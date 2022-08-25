import os

from parser import Parser
from transpiler import Transpiler
from symbol_table import SymbolTable

class Assembler:

    @classmethod
    def assemble(self, source_path):
        source_dir = os.path.dirname(source_path)
        source_basename = os.path.basename(source_path)
        source_name, ext = os.path.splitext(source_basename)
        if not ext == '.asm':
            raise ValueError('Input must be .asm file')

        target_path = (f'{source_dir}/{source_name}.hack')

        symbol_table = SymbolTable()

        # first pass
        with open(source_path, 'r') as source_file:
            line_number = 0
            for assembly in source_file:
                tokens = Parser.parse(assembly)
                if 'blank' in tokens:
                    continue
                if 'label' in tokens:
                    symbol_table.set(tokens['label'], line_number)
                    continue
                line_number += 1

        # second pass
        with open(source_path, 'r') as source_file:
            with open(target_path, 'w') as target_file:
                for assembly in source_file:
                    tokens = Parser.parse(assembly)
                    if 'blank' in tokens:
                        continue
                    if 'label' in tokens:
                        continue

                    try:
                        Transpiler.validate(tokens, symbol_table)
                        output = Transpiler.transpile(tokens, symbol_table)
                    except ValueError as err:
                        output = f"{assembly.strip()} // {err.args[0]}"

                    target_file.write(f"{output}\n")
