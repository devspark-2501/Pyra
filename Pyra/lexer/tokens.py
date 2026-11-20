
# PYRA - Token Definitions


class Token:
    def __init__(self, token_type, value, line, column):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


# Keywords
LET = "LET"
PRINT = "PRINT"
IF = "IF"
ELSE = "ELSE"
WHILE = "WHILE"
FN = "FN"
RETURN = "RETURN"

TRUE = "TRUE"
FALSE = "FALSE"

# Data Types
NUMBER = "NUMBER"
STRING = "STRING"
IDENTIFIER = "IDENTIFIER"

# Arithmetic Operators
PLUS = "PLUS"
MINUS = "MINUS"
MULTIPLY = "MULTIPLY"
DIVIDE = "DIVIDE"
MODULO = "MODULO"

# Assignment and Comparison Operators
EQUALS = "EQUALS"
EQUAL_EQUAL = "EQUAL_EQUAL"
NOT_EQUAL = "NOT_EQUAL"

GREATER = "GREATER"
LESS = "LESS"
GREATER_EQUAL = "GREATER_EQUAL"
LESS_EQUAL = "LESS_EQUAL"

# Logical Operators
AND = "AND"
OR = "OR"
NOT = "NOT"

# Symbols
LPAREN = "LPAREN"
RPAREN = "RPAREN"

LBRACE = "LBRACE"
RBRACE = "RBRACE"

COMMA = "COMMA"

# Special Token
EOF = "EOF"
