
# PYRA - Main Entry Point

from lexer.lexer import Lexer
from parser.parser import Parser
from interpreter.interpreter import Interpreter


def run(source_code):

    # Stage 1: Lexical Analysis
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    # Stage 2: Syntax Analysis
    parser = Parser(tokens)
    syntax_tree = parser.parse()

    # Stage 3: Execution
    interpreter = Interpreter()
    interpreter.interpret(syntax_tree)


source_code = """
let age = 16 + 5
print(age)

let count = 0

while count < 3 {
    print(count)
    count = count + 1
}

fn add(a, b) {
    return a + b
}

let result = add(10, 20)
print(result)

if result >= 30 {
    print("PYRA is working!")
} else {
    print("Something went wrong")
}
"""

run(source_code)
