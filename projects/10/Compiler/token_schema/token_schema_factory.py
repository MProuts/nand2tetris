from type_token_schema import TypeTokenSchema
from type_value_token_schema import TypeValueTokenSchema
from type_values_token_schema import TypeValuesTokenSchema
from one_of_token_schema import OneOfTokenSchema

class TokenSchemaFactory:

    VALID_KEYS = [
        "one_of",
        # "until"
    ]

    VALID_ARGS_TYPES = [ list, dict ]

    def create_all(self, list_of_args):
        mapped = map(
            lambda args: self.create(args),
            list_of_args)
        return list(mapped)

    def create(self, args):
        # list arguments
        # ===============
        if isinstance(args, list):
            length = len(args)

            # validation
            if length != 2:
                msg = f"Expected list with 2 items, got {length}: {args}"
                raise ValueError(msg)
            elif None in args:
                msg = f"List items must not be None, got: {args}"
                raise ValueError(msg)

            # instatiation
            token_type = args[0]
            token_value = args[1]
            if token_value == '*':
                return TypeTokenSchema(token_type)
            elif isinstance(token_value, list):
                return TypeValuesTokenSchema(token_type, token_value)
            else:
                return TypeValueTokenSchema(token_type, token_value)

        # dict arguments
        # ==============
        elif isinstance(args, dict):
            args_keys = args.keys()
            length = len(args_keys)
            key = list(args_keys)[0]

            # validation
            if length != 1:
                valid_keys = self._keys_to_enum_str(self.VALID_KEYS)
                received_keys = self._keys_to_list_str(args_keys)
                msg = f"Expected 1 key in '{valid_keys}', got {length} keys: {received_keys}"
                raise ValueError(msg)
            # TODO: move this into else below, get rid of VALID_KEYS
            elif not key in self.VALID_KEYS:
                valid_keys = self._keys_to_enum_str(self.VALID_KEYS)
                msg = f"Expected key in '{valid_keys}', got '{key}'"
                raise ValueError(msg)

            # instatiation
            if key == 'one_of':
                args1 = args[key][0]
                args2 = args[key][1]
                schema1 = self.create(args1)
                schema2 = self.create(args2)
                return OneOfTokenSchema(schema1, schema2)
        else:
            args_type_name = type(args).__name__
            msg = f"Expected list or dict, got {args_type_name}"
            raise ValueError(msg)

    def _keys_to_enum_str(self, keys):
        joined = "|".join(keys)
        return f"({joined})"

    def _keys_to_list_str(self, keys):
        mapped = map(lambda k: f"'{k}'", keys)
        joined = ', '.join(mapped)
        return joined
