from mako.template import Template

from path_helper import template_dir

class Translator:
    BINARY_OPERATORS = {
        'add': '+',
        'sub': '-',
        'and': '&',
        'or': '|'
    }

    UNARY_OPERATORS = {
        'neg': '-',
        'not': '!'
    }

    COMPARISON_OPERATORS = {
        'eq': 'JEQ',
        'lt': 'JLT',
        'gt': 'JGT'
    }

    TEMP_BASE_ADDRESS = 5
    # Base address of the 'pointer' segment
    POINTER_BASE_ADDRESS = 3

    # Address of a pointer to the base address of each segment
    POINTER_ADDRESSES = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
    }

    @classmethod
    def translate(self, tokens, line_number=0, source_name=None):

        # Arithmetic Operations
        # =====================
        command = tokens['command']
        if command in self.BINARY_OPERATORS.keys():
            operator = self.BINARY_OPERATORS[command]
            template = 'binary_operation'
            return self._render(template, operator=operator)

        if command in ['neg', 'not']:
            operator = self.UNARY_OPERATORS[command]
            template = 'unary_operation'
            return self._render(template, operator=operator)

        if command in ['eq', 'lt', 'gt']:
            operator = self.COMPARISON_OPERATORS[command]
            template = 'comparison_operation'
            return self._render(template,
                               operator=operator,
                               line_number=line_number)

        # Memory Operations
        # =================
        segment = tokens['arg1']
        index   = tokens['arg2']
        if command in ['push', 'pop']:
            if command == 'push' and segment == 'constant':
                return self._render('push_constant', const=index)

            if segment in self.POINTER_ADDRESSES.keys():
                template = f'{command}_pointer_address'
                pointer_addr = self.POINTER_ADDRESSES[segment]
                return self._render(template,
                                   pointer_addr=pointer_addr,
                                   index=index)

            if segment in ['temp', 'pointer', 'static']:
                template = f'{command}_address'
                addr = self._calculate_address(segment, index, source_name)
                return self._render(template, addr=addr)

            raise ValueError(f"Invalid segment '{command} {segment}'")

        raise ValueError(f"Invalid command '{command}'")

    @classmethod
    def _render(self, template, **locals):
        template = Template(filename=f'{template_dir}/{template}.mako')
        return template.render(**locals)

    @classmethod
    def _calculate_address(self, segment, index, source_name):
        index = self._coerce_index(index)
        if segment == 'temp':
            return self.TEMP_BASE_ADDRESS + index
        elif segment == 'pointer':
            return self.POINTER_BASE_ADDRESS + index
        elif segment == 'static':
            return f"{source_name}.{index}"

    @classmethod
    def _coerce_index(self, index):
        try:
            return int(index)
        except ValueError:
            raise ValueError(
                f"Invalid index '{index}'. Must be an integer."
            )
