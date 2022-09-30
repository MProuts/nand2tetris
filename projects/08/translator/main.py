from pathlib import Path

from parser import Parser
from translator import Translator
from template_helper import render

def _write_paragraph(file, string):
    file.write(string + "\n")

def _write_line(file, string):
    file.write(string)

def execute(source_path):
    source_path = Path(source_path)
    translator = Translator()

    # Validation
    if not source_path.is_file() and not source_path.is_dir():
        raise ValueError("Invalid source source_path. Must be a file or directory.")

    # Setup - file
    elif source_path.is_file():
        source_file_path = source_path
        source_dir_path = source_file_path.parents[0]
        source_file_paths = [ source_path ]
        if not source_file_path.suffix == '.vm':
            raise ValueError('Input must be .vm file')
        target_file_path = f'{source_dir_path}/{source_file_path.stem}.asm'

    # Setup - directory
    elif source_path.is_dir():
        source_dir_path = source_path
        source_file_paths = [path for path in source_dir_path.iterdir() if path.suffix == '.vm']
        if len(source_file_paths) == 0:
            raise ValueError('Directory must contain .vm file')
        target_file_path = f'{source_dir_path}/{source_dir_path.name}.asm'

    # Bootstrapping
    with open(target_file_path, 'w') as target_file:
        bootstrapping_header = render('layout/section_header', text="boostrapping")
        _write_paragraph(target_file, bootstrapping_header)

        bootstrapping = translator.bootstrapping_asm()
        _write_paragraph(target_file, bootstrapping)

        line_number = 0

        # File processing
        for source_file_path in source_file_paths:
            file_path_header = render('layout/section_header', text=source_file_path.as_posix())
            _write_paragraph(target_file, file_path_header)

            with open(source_file_path, 'r') as source_file:
                for line in source_file:
                    tokens = Parser.parse(line)
                    if 'blank' in tokens:
                        continue

                    # Include source line as comment above each line translation
                    comment = render('layout/comment', text=line.strip())
                    _write_line(target_file, comment)

                    try:
                        translation = translator.translate(
                            tokens,
                            line_number,
                            source_file_path.stem)
                    except ValueError as err:
                        translation = render('value_error', line=line, err=err)

                    _write_paragraph(target_file, translation)
                    line_number += 1
