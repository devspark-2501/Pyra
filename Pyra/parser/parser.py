
# PYRA - Syntax Parser

from lexer.tokens import (
    LET, PRINT, IF, ELSE, WHILE, FN, RETURN,
    TRUE, FALSE,
    NUMBER, STRING, IDENTIFIER,
    PLUS, MINUS, MULTIPLY, DIVIDE, MODULO,
    EQUALS, EQUAL_EQUAL, NOT_EQUAL,
    GREATER, LESS, GREATER_EQUAL, LESS_EQUAL,
    AND, OR, NOT,
    LPAREN, RPAREN, LBRACE, RBRACE, COMMA,
    EOF
)

from .nodes import (
    NumberNode,
    StringNode,
    BooleanNode,
    VariableNode,
    VariableDeclarationNode,
    AssignmentNode,
    BinaryOperationNode,
    UnaryOperationNode,
    FunctionCallNode,
    PrintNode,
    ExpressionStatementNode,
    BlockNode,
    IfNode,
    WhileNode,
    FunctionDeclarationNode,
    ReturnNode,
    ProgramNode
)


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    # =========================
    # TOKEN MANAGEMENT
    # =========================

    def current_token(self):
        if self.position >= len(self.tokens):
            return None

        return self.tokens[self.position]

    def peek(self):
        next_position = self.position + 1

        if next_position >= len(self.tokens):
            return None

        return self.tokens[next_position]

    def advance(self):
        token = self.current_token()

        if token is not None:
            self.position += 1

        return token

    def match(self, *token_types):
        token = self.current_token()

        if token is not None and token.type in token_types:
            self.advance()
            return True

        return False

    def consume(self, token_type, message):
        token = self.current_token()

        if token is None or token.type != token_type:
            line = token.line if token else "unknown"
            column = token.column if token else "unknown"

            raise SyntaxError(
                f"{message} at line {line}, column {column}"
            )

        return self.advance()

    # =========================
    # PROGRAM
    # =========================

    def parse(self):
        statements = []

        while self.current_token() is not None:
            if self.current_token().type == EOF:
                break

            statements.append(self.parse_statement())

        return ProgramNode(statements)

    # =========================
    # STATEMENTS
    # =========================

    def parse_statement(self):

        if self.match(LET):
            return self.parse_variable_declaration()

        if self.match(PRINT):
            return self.parse_print()

        if self.match(IF):
            return self.parse_if()

        if self.match(WHILE):
            return self.parse_while()

        if self.match(FN):
            return self.parse_function_declaration()

        if self.match(RETURN):
            return self.parse_return()

        if (
            self.current_token().type == IDENTIFIER
            and self.peek() is not None
            and self.peek().type == EQUALS
        ):
            return self.parse_assignment()

        return ExpressionStatementNode(
            self.parse_expression()
        )

    # =========================
    # VARIABLE DECLARATION
    # =========================

    def parse_variable_declaration(self):

        name = self.consume(
            IDENTIFIER,
            "Expected variable name"
        ).value

        self.consume(
            EQUALS,
            "Expected '=' after variable name"
        )

        value = self.parse_expression()

        return VariableDeclarationNode(name, value)

    # =========================
    # ASSIGNMENT
    # =========================

    def parse_assignment(self):

        name = self.advance().value

        self.consume(
            EQUALS,
            "Expected '=' in assignment"
        )

        value = self.parse_expression()

        return AssignmentNode(name, value)

    # =========================
    # PRINT
    # =========================

    def parse_print(self):

        self.consume(
            LPAREN,
            "Expected '(' after print"
        )

        expression = self.parse_expression()

        self.consume(
            RPAREN,
            "Expected ')' after print expression"
        )

        return PrintNode(expression)

    # =========================
    # IF / ELSE
    # =========================

    def parse_if(self):

        condition = self.parse_expression()

        then_branch = self.parse_block()

        else_branch = None

        if self.match(ELSE):
            else_branch = self.parse_block()

        return IfNode(
            condition,
            then_branch,
            else_branch
        )

    # =========================
    # WHILE LOOP
    # =========================

    def parse_while(self):

        condition = self.parse_expression()

        body = self.parse_block()

        return WhileNode(condition, body)

    # =========================
    # BLOCK
    # =========================

    def parse_block(self):

        self.consume(
            LBRACE,
            "Expected '{' to start block"
        )

        statements = []

        while (
            self.current_token() is not None
            and self.current_token().type != RBRACE
            and self.current_token().type != EOF
        ):
            statements.append(self.parse_statement())

        self.consume(
            RBRACE,
            "Expected '}' to close block"
        )

        return BlockNode(statements)

    # =========================
    # FUNCTION DECLARATION
    # =========================

    def parse_function_declaration(self):

        name = self.consume(
            IDENTIFIER,
            "Expected function name"
        ).value

        self.consume(
            LPAREN,
            "Expected '(' after function name"
        )

        parameters = []

        if self.current_token().type != RPAREN:

            parameters.append(
                self.consume(
                    IDENTIFIER,
                    "Expected parameter name"
                ).value
            )

            while self.match(COMMA):

                parameters.append(
                    self.consume(
                        IDENTIFIER,
                        "Expected parameter name"
                    ).value
                )

        self.consume(
            RPAREN,
            "Expected ')' after parameters"
        )

        body = self.parse_block()

        return FunctionDeclarationNode(
            name,
            parameters,
            body
        )

    # =========================
    # RETURN
    # =========================

    def parse_return(self):

        if (
            self.current_token() is None
            or self.current_token().type in (RBRACE, EOF)
        ):
            return ReturnNode()

        value = self.parse_expression()

        return ReturnNode(value)

    # =========================
    # EXPRESSIONS
    # =========================

    def parse_expression(self):
        return self.parse_or()

    # Logical OR
    def parse_or(self):

        node = self.parse_and()

        while self.match(OR):
            operator = OR
            right = self.parse_and()

            node = BinaryOperationNode(
                node,
                operator,
                right
            )

        return node

    # Logical AND
    def parse_and(self):

        node = self.parse_equality()

        while self.match(AND):
            operator = AND
            right = self.parse_equality()

            node = BinaryOperationNode(
                node,
                operator,
                right
            )

        return node

    # Equality
    def parse_equality(self):

        node = self.parse_comparison()

        while self.match(EQUAL_EQUAL, NOT_EQUAL):

            operator = self.tokens[self.position - 1].type

            right = self.parse_comparison()

            node = BinaryOperationNode(
                node,
                operator,
                right
            )

        return node

    # Comparison
    def parse_comparison(self):

        node = self.parse_term()

        while self.match(
            GREATER,
            LESS,
            GREATER_EQUAL,
            LESS_EQUAL
        ):

            operator = self.tokens[self.position - 1].type

            right = self.parse_term()

            node = BinaryOperationNode(
                node,
                operator,
                right
            )

        return node

    # Addition and subtraction
    def parse_term(self):

        node = self.parse_factor()

        while self.match(PLUS, MINUS):

            operator = self.tokens[self.position - 1].type

            right = self.parse_factor()

            node = BinaryOperationNode(
                node,
                operator,
                right
            )

        return node

    # Multiplication, division and modulo
    def parse_factor(self):

        node = self.parse_unary()

        while self.match(MULTIPLY, DIVIDE, MODULO):

            operator = self.tokens[self.position - 1].type

            right = self.parse_unary()

            node = BinaryOperationNode(
                node,
                operator,
                right
            )

        return node

    # Unary operations
    def parse_unary(self):

        if self.match(MINUS, NOT):

            operator = self.tokens[self.position - 1].type

            operand = self.parse_unary()

            return UnaryOperationNode(
                operator,
                operand
            )

        return self.parse_primary()

    # =========================
    # PRIMARY EXPRESSIONS
    # =========================

    def parse_primary(self):

        token = self.current_token()

        if token is None:
            raise SyntaxError("Unexpected end of expression")

        if token.type == NUMBER:
            self.advance()
            return NumberNode(token.value)

        if token.type == STRING:
            self.advance()
            return StringNode(token.value)

        if token.type == TRUE:
            self.advance()
            return BooleanNode(True)

        if token.type == FALSE:
            self.advance()
            return BooleanNode(False)

        if token.type == IDENTIFIER:

            name = self.advance().value

            # Function call
            if self.match(LPAREN):

                arguments = []

                if self.current_token().type != RPAREN:

                    arguments.append(
                        self.parse_expression()
                    )

                    while self.match(COMMA):

                        arguments.append(
                            self.parse_expression()
                        )

                self.consume(
                    RPAREN,
                    "Expected ')' after function arguments"
                )

                return FunctionCallNode(
                    name,
                    arguments
                )

            return VariableNode(name)

        # Parenthesized expression
        if self.match(LPAREN):

            expression = self.parse_expression()

            self.consume(
                RPAREN,
                "Expected ')' after expression"
            )

            return expression

        raise SyntaxError(
            f"Unexpected token '{token.value}' "
            f"at line {token.line}, column {token.column}"
        )
