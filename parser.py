class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', None)

    def eat(self, token_type, token_value=None):
        token = self.current_token()
        if token[0] == token_type and (token_value is None or token[1] == token_value):
            self.pos += 1
            return token
        else:
            raise SyntaxError(f'Expected token {token_type}{" with value "+str(token_value) if token_value else ""}, got {token}')

    def parse(self):
        return self.parse_statements()

    def parse_statements(self):
        stmts = []
        while self.current_token()[0] != 'EOF':
            stmts.append(self.parse_statement())
        return ('Statements', stmts)

    def parse_statement(self):
        token = self.current_token()
        if token[0] == 'WHILE':
            return self.parse_while()
        elif token[0] == 'IF':
            return self.parse_if()
        elif token[0] == 'ID' and self.peek_next_token()[0] == 'OP' and self.peek_next_token()[1] == '=':
            return self.parse_assignment()
        else:
            return self.parse_expression()

    def peek_next_token(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return ('EOF', None)

    def parse_while(self):
        self.eat('WHILE')
        condition = self.parse_expression()
        self.eat('COLON')
        body = self.parse_statement()
        return ('While', condition, body)

    def parse_if(self):
        self.eat('IF')
        condition = self.parse_expression()
        self.eat('COLON')
        then_body = self.parse_statement()
        else_body = None
        if self.current_token()[0] == 'ELSE':
            self.eat('ELSE')
            self.eat('COLON')
            else_body = self.parse_statement()
        return ('If', condition, then_body, else_body)

    def parse_assignment(self):
        var_token = self.eat('ID')
        self.eat('OP', '=')
        expr = self.parse_expression()
        return ('Assign', var_token[1], expr)

    # نبدأ بتعديل هنا لدعم المقارنات

    def parse_expression(self):
        # أولًا نحلل الجانب الأيسر كعملية حسابية
        left = self.parse_arithmetic_expression()

        # بعدين نبحث عن عمليات مقارنة
        while self.current_token()[0] == 'OP' and self.current_token()[1] in ('<', '>', '<=', '>=', '==', '!='):
            op = self.eat('OP')[1]
            right = self.parse_arithmetic_expression()
            left = ('BinOp', op, left, right)
        return left

    def parse_arithmetic_expression(self):
        left = self.parse_term()
        while self.current_token()[0] == 'OP' and self.current_token()[1] in ('+', '-'):
            op = self.eat('OP')[1]
            right = self.parse_term()
            left = ('BinOp', op, left, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token()[0] == 'OP' and self.current_token()[1] in ('*', '/'):
            op = self.eat('OP')[1]
            right = self.parse_factor()
            left = ('BinOp', op, left, right)
        return left

    def parse_factor(self):
        token = self.current_token()
        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return ('Number', token[1])
        elif token[0] == 'ID':
            self.eat('ID')
            return ('ID', token[1])
        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            expr = self.parse_expression()
            self.eat('RPAREN')
            return expr
        else:
            raise SyntaxError(f'Unexpected token in factor: {token}')













