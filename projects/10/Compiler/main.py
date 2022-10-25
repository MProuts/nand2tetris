from pathlib import Path

from tokenizer import Tokenizer

# NOTE: I haven't tested this class to ensure it works. Since I've written unit
# tests, and this is just utility for manual testing, I'm not going to bother
# finishing it. I'm keeping it in version control in case it's helpful in
# later chapters.
def execute(source_path):
    raise NotImplemented

    # source_path = Path(source_path)
    # translator = Translator()

    # # Validation
    # if source_path and not source_path.is_file() and not source_path.is_dir():
    #     raise ValueError(f"Invalid source {source_path}. Must be a file or directory.")

    # # Setup - file
    # elif source_path.is_file():
    #     source_file_path = source_path
    #     source_dir_path = source_file_path.parents[0]
    #     source_file_paths = [ source_path ]
    #     if not source_file_path.suffix == '.jack':
    #         raise ValueError('Input must be .jack file')
    #     target_file_path = f'{source_dir_path}/{source_file_path.stem}.xml'

    # # Setup - directory
    # elif source_path.is_dir():
    #     source_dir_path = source_path
    #     source_file_paths = [path for path in source_dir_path.iterdir() if path.suffix == '.jack']
    #     if len(source_file_paths) == 0:
    #         raise ValueError('Directory must contain .jack file')
    #     target_file_path = f'{source_dir_path}/{source_dir_path.name}.xml'

    # # Processing
    # with open(target_file_path, 'w') as target_file:
    #     for source_file_path in source_file_paths:
    #         with open(source_file_path, 'r') as source_file:

    #             tokenizer = JackTokenizer(source_file_path=source_file_path)
    #             parser = JackParser(tokenizer.token_gen(), io=target_file)

    #             try:
    #                 parser.compile_class()

    #             except ValueError as err:
    #                 print(f"ValueError: {err.args[0]}")

    #             line_number += 1
