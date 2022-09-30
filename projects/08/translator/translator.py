from template_helper import render

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

    # Allow setting initial return_index for testing
    def __init__(self, return_index=0):
        self.return_index = return_index

    def bootstrapping_asm(self):
        call_asm = self.translate({
            'command': 'call',
            'arg1': 'Sys.init',
            'arg2': '0',
        })
        return render('bootstrapping', call_asm=call_asm.strip())

    def translate(self, tokens, line_number=0, source_name=None):

        command = tokens['command']

        # Arithmetic Commands
        # ===================
        if command in self.BINARY_OPERATORS.keys():
            operator = self.BINARY_OPERATORS[command]
            template = 'binary_operation'
            return render(template, operator=operator)

        if command in ['neg', 'not']:
            operator = self.UNARY_OPERATORS[command]
            template = 'unary_operation'
            return render(template, operator=operator)

        if command in ['eq', 'lt', 'gt']:
            operator = self.COMPARISON_OPERATORS[command]
            template = 'comparison_operation'
            return render(template,
                          operator=operator,
                          line_number=line_number)

        # Memory Commands
        # ===============
        if command in ['push', 'pop']:
            segment = tokens['arg1']
            index   = tokens['arg2']

            if segment == 'constant' and command == 'push':
                return render('push_constant', const=index)

            if segment in self.POINTER_ADDRESSES.keys():
                template = f'{command}_pointer_address'
                pointer_addr = self.POINTER_ADDRESSES[segment]
                return render(template,
                              pointer_addr=pointer_addr,
                              index=index)

            if segment in ['temp', 'pointer', 'static']:
                template = f'{command}_address'
                addr = self._calculate_address(segment, index, source_name)
                return render(template, addr=addr)

            raise ValueError(f"Invalid segment '{command} {segment}'")

        # Branching Commands
        # ==================
        if command == 'label':
            template = 'label'
            symbol = tokens['arg1']
            return render(template, symbol=symbol)

        if command == 'if-goto':
            template = 'if_goto'
            symbol= tokens['arg1']
            return render(template, symbol=symbol)

        if command == 'goto':
            template = 'goto'
            symbol = tokens['arg1']
            return render(template, symbol=symbol)

        # Function Commands
        # =================
        if command == 'function':
            template = 'function'
            symbol = tokens['arg1']
            nvars = self._to_int(tokens['arg2'])
            return render(template, symbol=symbol, nvars=nvars)

        if command == 'return':
            template = 'return'
            temp_0 = self.TEMP_BASE_ADDRESS
            temp_1 = self.TEMP_BASE_ADDRESS + 1
            return render(template, temp_0=temp_0, temp_1=temp_1)

        if command == 'call':
            template = 'call'
            symbol = tokens['arg1'] # symbol already includes filename
            n_args = tokens['arg2']
            return_addr = f"{symbol}$ret.{self.return_index}"
            assembly = render(
                template,
                symbol=symbol,
                n_args=n_args,
                return_addr=return_addr)
            self.return_index += 1
            return assembly

        # Unrecognized command
        # ====================
        raise ValueError(f"Invalid command '{command}'")

    def _calculate_address(self, segment, index, source_name):
        if segment == 'temp':
            return self.TEMP_BASE_ADDRESS + self._to_int(index)
        elif segment == 'pointer':
            return self.POINTER_BASE_ADDRESS + self._to_int(index)
        elif segment == 'static':
            return f"{source_name}.{index}"

    def _to_int(self, string):
        try:
            return int(string)
        except ValueError:
            raise ValueError(
                f"Invalid value '{string}'. Must be an integer."
            )
