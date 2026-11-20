
# PYRA - Main Entry Point

from lexer.lexer import Lexer
from parser.parser import Parser


def run(source_code):

    # Stage 1: Lexical Analysis
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    # Stage 2: Syntax Analysis
    parser = Parser(tokens)
    syntax_tree = parser.parse()

    print("PYRA: Parsing successful!")
    print("Total statements:", len(syntax_tree.statements))


source_code = """
let name = "Tanush"
let age = 16

let result = 10 + 20 * 3

print(name)
print(result)

if age >= 16 {
    print("Welcome to Pyra!")
}
"""

run(source_code)
