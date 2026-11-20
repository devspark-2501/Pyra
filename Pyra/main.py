
# PYRA - Programming Language Interpreter

from lexer.lexer import Lexer


def run(source_code):
    # Step 1: Create Lexer
    lexer = Lexer(source_code)

    # Step 2: Convert source code into tokens
    tokens = lexer.tokenize()

    # Step 3: Display tokens
    for token in tokens:
        print(token)


# Test Pyra source code
source_code = """
let age = 16 + 5
print(age)
"""

run(source_code)
