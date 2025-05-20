import re

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.tokens = []

        self.keywords = {'while', 'if', 'else', 'for'}

        self.token_specification = [
            ('NUMBER',   r'\d+'),
            ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),
            ('STRING',   r'"([^"\\]|\\.)*"'),
            ('NEWLINE',  r'\n'),
            ('SKIP',     r'[ \t]+'),
            ('OP',       r'==|!=|<=|>=|<|>|=|\+|-|\*|/'),
            ('COLON',    r':'),
            ('LPAREN',   r'\('),
            ('RPAREN',   r'\)'),
            ('UNKNOWN',  r'.'),
        ]
        self.token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)

    def tokenize(self):
        for mo in re.finditer(self.token_regex, self.source):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'ID' and value in self.keywords:
                self.tokens.append((value.upper(), value))  # كلمات مفتاحية
            elif kind == 'NUMBER':
                value = int(value)
                self.tokens.append(('NUMBER', value))
            elif kind == 'ID':
                self.tokens.append(('ID', value))
            elif kind == 'STRING':
                self.tokens.append(('STRING', value))
            elif kind == 'NEWLINE':
                pass  # ممكن تتجاهل
            elif kind == 'SKIP':
                continue
            elif kind == 'OP':
                self.tokens.append(('OP', value))
            elif kind == 'COLON':
                self.tokens.append(('COLON', value))
            elif kind == 'LPAREN':
                self.tokens.append(('LPAREN', value))
            elif kind == 'RPAREN':
                self.tokens.append(('RPAREN', value))
            else:
                raise SyntaxError(f'Unknown token: {value}')
        self.tokens.append(('EOF', None))
        return self.tokens









