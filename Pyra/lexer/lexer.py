
# PYRA - Lexical Analyzer

from .tokens import (
    Token,
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


class Lexer:
    KEYWORDS = {
        "let": LET,
        "print": PRINT,
        "if": IF,
        "else": ELSE,
        "while": WHILE,
        "fn": FN,
        "return": RETURN,
        "true": TRUE,
        "false": FALSE,
        "and": AND,
        "or": OR,
        "not": NOT
    }

    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    # Get the current character
    def current_char(self):
        if self.position >= len(self.source):
            return None

        return self.source[self.position]

    # Look at the next character
    def peek(self):
        next_position = self.position + 1

        if next_position >= len(self.source):
            return None

        return self.source[next_position]

    # Move to the next character
    def advance(self):
        char = self.current_char()

        if char is None:
            return None

        self.position += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char

    # Add a token to our token list
    def add_token(self, token_type, value, line, column):
        self.tokens.append(
            Token(token_type, value, line, column)
        )

    # Skip spaces, tabs and newlines
    def skip_whitespace(self):
        while self.current_char() in (" ", "\t", "\r", "\n"):
            self.advance()

    # Read numbers
    def read_number(self):
        start_line = self.line
        start_column = self.column

        number = ""

        while self.current_char() is not None and self.current_char().isdigit():
            number += self.advance()

        if self.current_char() == "." and self.peek() is not None and self.peek().isdigit():
            number += self.advance()

            while self.current_char() is not None and self.current_char().isdigit():
                number += self.advance()

            value = float(number)
        else:
            value = int(number)

        self.add_token(NUMBER, value, start_line, start_column)

    # Read identifiers and keywords
    def read_identifier(self):
        start_line = self.line
        start_column = self.column

        identifier = ""

        while self.current_char() is not None and (
            self.current_char().isalnum() or self.current_char() == "_"
        ):
            identifier += self.advance()

        token_type = self.KEYWORDS.get(identifier, IDENTIFIER)

        if token_type == TRUE:
            value = True
        elif token_type == FALSE:
            value = False
        else:
            value = identifier

        self.add_token(
            token_type,
            value,
            start_line,
            start_column
        )

    # Read strings
    def read_string(self):
        start_line = self.line
        start_column = self.column

        quote = self.advance()
        value = ""

        while self.current_char() is not None:
            char = self.current_char()

            if char == quote:
                self.advance()

                self.add_token(
                    STRING,
                    value,
                    start_line,
                    start_column
                )
                return

            if char == "\n":
                raise SyntaxError(
                    f"Unterminated string at line {start_line}, column {start_column}"
                )

            if char == "\\":
                self.advance()
                escaped = self.current_char()

                if escaped is None:
                    break

                escape_sequences = {
                    "n": "\n",
                    "t": "\t",
                    "r": "\r",
                    '"': '"',
                    "'": "'",
                    "\\": "\\"
                }

                if escaped not in escape_sequences:
                    raise SyntaxError(
                        f"Invalid escape sequence at line {self.line}, column {self.column}"
                    )

                value += escape_sequences[escaped]
                self.advance()

            else:
                value += self.advance()

        raise SyntaxError(
            f"Unterminated string at line {start_line}, column {start_column}"
        )

    # Skip single-line comments
    def skip_comment(self):
        while self.current_char() is not None and self.current_char() != "\n":
            self.advance()

    # Main tokenization method
    def tokenize(self):

        while self.current_char() is not None:

            char = self.current_char()

            if char in (" ", "\t", "\r", "\n"):
                self.skip_whitespace()
                continue

            if char == "#":
                self.skip_comment()
                continue

            start_line = self.line
            start_column = self.column

            # Numbers
            if char.isdigit():
                self.read_number()
                continue

            # Identifiers and keywords
            if char.isalpha() or char == "_":
                self.read_identifier()
                continue

            # Strings
            if char in ('"', "'"):
                self.read_string()
                continue

            # Two-character operators
            if char == "=" and self.peek() == "=":
                self.advance()
                self.advance()
                self.add_token(EQUAL_EQUAL, "==", start_line, start_column)

            elif char == "!" and self.peek() == "=":
                self.advance()
                self.advance()
                self.add_token(NOT_EQUAL, "!=", start_line, start_column)

            elif char == ">" and self.peek() == "=":
                self.advance()
                self.advance()
                self.add_token(GREATER_EQUAL, ">=", start_line, start_column)

            elif char == "<" and self.peek() == "=":
                self.advance()
                self.advance()
                self.add_token(LESS_EQUAL, "<=", start_line, start_column)

            # Single-character operators and symbols
            else:
                single_tokens = {
                    "+": PLUS,
                    "-": MINUS,
                    "*": MULTIPLY,
                    "/": DIVIDE,
                    "%": MODULO,
                    "=": EQUALS,
                    ">": GREATER,
                    "<": LESS,
                    "(": LPAREN,
                    ")": RPAREN,
                    "{": LBRACE,
                    "}": RBRACE,
                    ",": COMMA
                }

                if char not in single_tokens:
                    raise SyntaxError(
                        f"Unexpected character '{char}' "
                        f"at line {self.line}, column {self.column}"
                    )

                self.advance()

                self.add_token(
                    single_tokens[char],
                    char,
                    start_line,
                    start_column
                )

        self.add_token(EOF, None, self.line, self.column)

        return self.tokens
