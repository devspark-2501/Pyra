
# PYRA - Main Entry Point

import sys

from lexer.lexer import Lexer
from parser.parser import Parser
from interpreter.interpreter import Interpreter


def run(source_code):

    try:
        # Stage 1: Lexical Analysis
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        # Stage 2: Syntax Analysis
        parser = Parser(tokens)
        syntax_tree = parser.parse()

        # Stage 3: Execution
        interpreter = Interpreter()
        interpreter.interpret(syntax_tree)

    except Exception as error:
        print(error)


def run_file(file_path):

    if not file_path.endswith(".pyra"):
        print("PYRA Error: File must have a .pyra extension.")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            source_code = file.read()

        run(source_code)

    except FileNotFoundError:
        print(f"PYRA Error: File '{file_path}' not found.")

    except OSError as error:
        print(f"PYRA Error: Could not read file: {error}")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("PYRA Interpreter")
        print("Usage: python main.py <file.pyra>")

    else:
        run_file(sys.argv[1])
