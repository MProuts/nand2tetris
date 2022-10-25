from io import StringIO
from token_schema_factory import TokenSchemaFactory
from token_gen_wrapper import TokenGenWrapper

# keywords
# ========
keyword             = ['keyword', '*']
keyword_class       = ['keyword', 'class']
keyword_var         = ['keyword', 'var']
keyword_return      = ['keyword', 'return']
keyword_let         = ['keyword', 'let']
keyword_if          = ['keyword', 'if']
keyword_else        = ['keyword', 'else']
keyword_while       = ['keyword', 'while']
keyword_do          = ['keyword', 'do']
keyword_return      = ['keyword', 'return']
keyword_void        = ['keyword', 'void']
class_var_keyword   = ['keyword', ['static', 'field']]
type_keyword        = ['keyword', ['int', 'char', 'boolean']]
return_type_keyword = ['keyword', ['int', 'char', 'boolean', 'void']]
constant_keyword    = ['keyword', ['true', 'false', 'null', 'this']]
statement_keyword   = ['keyword', ['let', 'if', 'while', 'do', 'return']]
subroutine_keyword  = ['keyword', ['constructor', 'function', 'method']]

# symbols
# =======
o_bracket = ['symbol', '[']
c_bracket = ['symbol', ']']
o_curly   = ['symbol', '{']
c_curly   = ['symbol', '}']
o_paren   = ['symbol', '(']
c_paren   = ['symbol', ')']
dot       = ['symbol', '.']
comma     = ['symbol', ',']
semicolon = ['symbol', ';']
equals    = ['symbol', '=']
unary_op  = ['symbol', [ '~', '-' ] ]
op        = [ 'symbol', [ '+', '-', '*', '/', '&', '|', '~', '<', '>', '=', ] ]

# identifiers
# ===========
identifier = ['identifier', '*']

# constants
# =========
int_constant = ['integerConstant', '*']
str_constant = ['stringConstant', '*']

class JackParser:
    def __init__(self, token_gen, io=None):
        self.tokens = TokenGenWrapper(token_gen, initial_current=True)
        self.schema_factory = TokenSchemaFactory()
        self.io = io or StringIO("")

    def compile_class(self):
        self.io.write("<class>\n")
        self._assert_current(keyword_class)
        self._advance()
        self._assert_current(identifier)
        self._advance()
        self._assert_current(o_curly)
        self._advance()
        while self._match_current(class_var_keyword):
            self.compile_class_var_dec()
        while self._match_current(subroutine_keyword):
            self.compile_subroutine_dec()
        self._assert_current(c_curly)
        self._advance()
        self.io.write("</class>\n")

    def compile_class_var_dec(self):
        self.io.write("<classVarDec>\n")
        self._assert_current(class_var_keyword)
        self._advance()
        self._assert_current({ 'one_of': [ type_keyword, identifier ] })
        self._advance()
        self._assert_current(identifier)
        self._advance()

        while not self._match_current(semicolon):
            self._assert_current(comma)
            self._advance()
            self._assert_current(identifier)
            self._advance()

        # still need to advance past the semicolon
        self._advance()
        self.io.write("</classVarDec>\n")

    def compile_subroutine_dec(self):
        self.io.write("<subroutineDec>\n")
        self._assert_current(subroutine_keyword)
        self._advance()
        self._assert_current({ 'one_of': [ return_type_keyword, identifier ] })
        self._advance()
        self._assert_current(identifier)
        self._advance()
        self._assert_current(o_paren)
        self._advance()
        self.compile_parameter_list()
        self._assert_current(c_paren)
        self._advance()
        self.compile_subroutine_body()
        self.io.write("</subroutineDec>\n")

    def compile_parameter_list(self):
        self.io.write("<parameterList>\n")
        if not self._match_current(c_paren):
            self._assert_current({ 'one_of': [ type_keyword, identifier ] })
            self._advance()
            self._assert_current(identifier)
            self._advance()

            while not self._match_current(c_paren):
                self._assert_current(comma)
                self._advance()
                self._assert_current({ 'one_of': [ type_keyword, identifier ] })
                self._advance()
                self._assert_current(identifier)
                self._advance()

        self.io.write("</parameterList>\n")

    def compile_subroutine_body(self):
        self.io.write("<subroutineBody>\n")
        self._assert_current(o_curly)
        self._advance()
        while self._match_current(keyword_var):
            self.compile_var_dec()
        self.compile_statements()
        self._assert_current(c_curly)
        self._advance()
        self.io.write("</subroutineBody>\n")

    def compile_var_dec(self):
        self.io.write("<varDec>\n")
        if self._match_current(keyword_var):
            self._advance()
            self._assert_current({ 'one_of': [ type_keyword, identifier ] })
            self._advance()
            self._assert_current(identifier)
            self._advance()

            while not self._match_current(semicolon):
                self._assert_current(comma)
                self._advance()
                self._assert_current(identifier)
                self._advance()

            # still need to advance past the semicolon
            self._advance()
        self.io.write("</varDec>\n")

    def compile_statements(self):
        self.io.write("<statements>\n")

        while self.tokens.current and self._match_current(statement_keyword):
            if self._match_current(keyword_let):
                self.compile_let()
            elif self._match_current(keyword_if):
                self.compile_if()
            elif self._match_current(keyword_while):
                self.compile_while()
            elif self._match_current(keyword_do):
                self.compile_do()
            elif self._match_current(keyword_return):
                self.compile_return()

        self.io.write("</statements>\n")

    def compile_let(self):
        self.io.write("<letStatement>\n")
        self._assert_current(keyword_let)
        self._advance()
        self._assert_current(identifier)
        self._advance()
        if self._match_current(o_bracket):
            self._advance()
            self.compile_expression()
            self._assert_current(c_bracket)
            self._advance()
        self._assert_current(equals)
        self._advance()
        self.compile_expression()
        self._assert_current(semicolon)
        self._advance()
        self.io.write("</letStatement>\n")

    def compile_if(self):
        self.io.write("<ifStatement>\n")
        self._assert_current(keyword_if)
        self._advance()
        self._assert_current(o_paren)
        self._advance()
        self.compile_expression()
        self._assert_current(c_paren)
        self._advance()
        self._assert_current(o_curly)
        self._advance()
        self.compile_statements()
        self._assert_current(c_curly)
        self._advance()

        if self.tokens.current and self._match_current(keyword_else):
            self._advance()
            self._assert_current(o_curly)
            self._advance()
            self.compile_statements()
            self._assert_current(c_curly)
            self._advance()

        self.io.write("</ifStatement>\n")

    def compile_while(self):
        self.io.write("<whileStatement>\n")
        self._assert_current(keyword_while)
        self._advance()
        self._assert_current(o_paren)
        self._advance()
        self.compile_expression()
        self._assert_current(c_paren)
        self._advance()
        self._assert_current(o_curly)
        self._advance()
        self.compile_statements()
        self._assert_current(c_curly)
        self._advance()
        self.io.write("</whileStatement>\n")

    def compile_do(self):
        self.io.write("<doStatement>\n")
        self._assert_current(keyword_do)
        self._advance()
        self._assert_current(identifier)
        self._advance()
        self._assert_current({ 'one_of': [ o_paren, dot ] })

        # ( expression_list )
        if self._match_current(o_paren):
            self._advance()
            self.compile_expression_list()
            self._assert_current(c_paren)
            self._advance()

        # .identifier( expression_list )
        else:
            self._advance()
            self._assert_current(identifier)
            self._advance()
            self._assert_current(o_paren)
            self._advance()
            self.compile_expression_list()
            self._assert_current(c_paren)
            self._advance()

        self._assert_current(semicolon)
        self._advance()

        self.io.write("</doStatement>\n")

    def compile_return(self):
        self.io.write("<returnStatement>\n")
        self._assert_current(keyword_return)
        self._advance()
        if self._match_current(semicolon):
            self._advance()
        else:
            self.compile_expression()
            self._assert_current(semicolon)
            self._advance()

        self.io.write("</returnStatement>\n")

    def compile_expression(self):
        self.io.write("<expression>\n")
        self.compile_term()

        # EOF
        while self.tokens.current and self._match_current(op):
            self._advance()
            self.compile_term()

        self.io.write("</expression>\n")

    def compile_term(self):
        self.io.write("<term>\n")

        # int or str constants
        if self._match_current({ 'one_of': [ int_constant, str_constant ] }):
            self._advance()

        # keyword constant
        elif self._match_current(keyword):
            self._assert_current(constant_keyword)
            self._advance()

        # unary operator
        elif self._match_current(unary_op):
            self._advance()
            self.compile_term()

        # ( expression )
        elif self._match_current(o_paren):
            self._advance()
            self.compile_expression()
            self._assert_current(c_paren)
            self._advance()

        # identifier
        elif self._match_current(identifier):
            self._advance()

            # EOF
            if not self.tokens.current:
                pass

            # [ expression ]
            elif self._match_current(o_bracket):
                self._advance()
                self.compile_expression()
                self._assert_current(c_bracket)
                self._advance()

            # ( expression_list )
            elif self._match_current(o_paren):
                self._advance()
                self.compile_expression_list()
                self._assert_current(c_paren)
                self._advance()

            # .identifier( expression_list )
            elif self._match_current(dot):
                self._advance()
                self._assert_current(identifier)
                self._advance()
                self._assert_current(o_paren)
                self._advance()
                self.compile_expression_list()
                self._assert_current(c_paren)
                self._advance()

        self.io.write("</term>\n")

    def compile_expression_list(self):
        self.io.write("<expressionList>\n")
        # empty list
        if not self._match_current(c_paren):
            # first expression
            self.compile_expression()

            # following expressions
            while not self._match_current(c_paren):
                self._assert_current(comma)
                self._advance()
                self.compile_expression()
        self.io.write("</expressionList>\n")

    # private methods
    # ===============
    def _advance(self):
        xml = self.tokens.current.to_xml()
        self.io.write(xml + '\n')
        next(self.tokens)

    def _assert_current(self, schema_args):
        current_token = self.tokens.current
        schema = self.schema_factory.create(schema_args)
        return schema.assert_matches(current_token)

    def _match_current(self, schema_args):
        current_token = self.tokens.current
        schema = self.schema_factory.create(schema_args)
        return schema.matches(current_token)

    def _read(self):
        self.io.seek(0)
        return self.io.read()
