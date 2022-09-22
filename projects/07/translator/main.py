import os

from parser import Parser
from translator import Translator

class Main:

    @classmethod
    def execute(self, source_path):
        source_dir = os.path.dirname(source_path)
        source_basename = os.path.basename(source_path)
        source_name, ext = os.path.splitext(source_basename)
        if not ext == '.vm':
            raise ValueError('Input must be .vm file')
        target_path = f'{source_dir}/{source_name}.asm'

        with open(source_path, 'r') as source_file:
            with open(target_path, 'w') as target_file:
                line_number = 0
                for vm_code in source_file:
                    tokens = Parser.parse(vm_code)
                    if 'blank' in tokens:
                        continue

                    # Include comment with source vm code
                    target_file.write(f"// {vm_code}")

                    try:
                        output = Translator.translate(
                            tokens,
                            line_number,
                            source_name)
                    except ValueError as err:
                        output = f"{vm_code.strip()} // {err.args[0]}"

                    target_file.write(f"{output}\n")
                    line_number += 1

