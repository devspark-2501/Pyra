
# PYRA - Interpreter

from lexer.tokens import (
    PLUS, MINUS, MULTIPLY, DIVIDE, MODULO,
    EQUAL_EQUAL, NOT_EQUAL,
    GREATER, LESS, GREATER_EQUAL, LESS_EQUAL,
    AND, OR, NOT
)

from parser.nodes import (
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

from .environment import Environment
from .runtime_values import PyraFunction, ReturnSignal


class Interpreter:

    def __init__(self):
        self.environment = Environment()

    # =========================
    # PROGRAM EXECUTION
    # =========================

    def interpret(self, program):

        if not isinstance(program, ProgramNode):
            raise RuntimeError("Expected a PYRA program")

        for statement in program.statements:
            self.execute(statement)

    # =========================
    # STATEMENT EXECUTION
    # =========================

    def execute(self, node):

        # Variable declaration
        if isinstance(node, VariableDeclarationNode):

            value = self.evaluate(node.value)

            self.environment.define(
                node.name,
                value
            )

        # Variable assignment
        elif isinstance(node, AssignmentNode):

            value = self.evaluate(node.value)

            self.environment.assign(
                node.name,
                value
            )

        # Print statement
        elif isinstance(node, PrintNode):

            value = self.evaluate(node.expression)

            print(value)

        # Expression statement
        elif isinstance(node, ExpressionStatementNode):

            self.evaluate(node.expression)

        # If / else
        elif isinstance(node, IfNode):

            condition = self.evaluate(node.condition)

            if self.is_truthy(condition):
                self.execute_block(node.then_branch)
            elif node.else_branch is not None:
                self.execute_block(node.else_branch)

        # While loop
        elif isinstance(node, WhileNode):

            while self.is_truthy(
                self.evaluate(node.condition)
            ):
                self.execute_block(node.body)

        # Function declaration
        elif isinstance(node, FunctionDeclarationNode):

            function = PyraFunction(
                node,
                self.environment
            )

            self.environment.define(
                node.name,
                function
            )

        # Return statement
        elif isinstance(node, ReturnNode):

            value = None

            if node.value is not None:
                value = self.evaluate(node.value)

            raise ReturnSignal(value)

        else:
            raise RuntimeError(
                f"Unknown statement: {type(node).__name__}"
            )

    # =========================
    # BLOCK EXECUTION
    # =========================

    def execute_block(self, block):

        previous_environment = self.environment

        self.environment = self.environment.create_child()

        try:
            for statement in block.statements:
                self.execute(statement)

        finally:
            self.environment = previous_environment

    # =========================
    # EXPRESSION EVALUATION
    # =========================

    def evaluate(self, node):

        # Number
        if isinstance(node, NumberNode):
            return node.value

        # String
        if isinstance(node, StringNode):
            return node.value

        # Boolean
        if isinstance(node, BooleanNode):
            return node.value

        # Variable lookup
        if isinstance(node, VariableNode):
            return self.environment.get(node.name)

        # Binary operation
        if isinstance(node, BinaryOperationNode):
            return self.evaluate_binary(node)

        # Unary operation
        if isinstance(node, UnaryOperationNode):
            return self.evaluate_unary(node)

        # Function call
        if isinstance(node, FunctionCallNode):
            return self.call_function(node)

        raise RuntimeError(
            f"Unknown expression: {type(node).__name__}"
        )

    # =========================
    # BINARY OPERATIONS
    # =========================

    def evaluate_binary(self, node):

        left = self.evaluate(node.left)

        # Logical AND
        if node.operator == AND:

            if not self.is_truthy(left):
                return False

            return self.is_truthy(
                self.evaluate(node.right)
            )

        # Logical OR
        if node.operator == OR:

            if self.is_truthy(left):
                return True

            return self.is_truthy(
                self.evaluate(node.right)
            )

        right = self.evaluate(node.right)

        if node.operator == PLUS:
            return left + right

        if node.operator == MINUS:
            return left - right

        if node.operator == MULTIPLY:
            return left * right

        if node.operator == DIVIDE:
            return left / right

        if node.operator == MODULO:
            return left % right

        if node.operator == EQUAL_EQUAL:
            return left == right

        if node.operator == NOT_EQUAL:
            return left != right

        if node.operator == GREATER:
            return left > right

        if node.operator == LESS:
            return left < right

        if node.operator == GREATER_EQUAL:
            return left >= right

        if node.operator == LESS_EQUAL:
            return left <= right

        raise RuntimeError("Unknown binary operator")

    # =========================
    # UNARY OPERATIONS
    # =========================

    def evaluate_unary(self, node):

        value = self.evaluate(node.operand)

        if node.operator == MINUS:
            return -value

        if node.operator == NOT:
            return not self.is_truthy(value)

        raise RuntimeError("Unknown unary operator")

    # =========================
    # FUNCTION CALLS
    # =========================

    def call_function(self, node):

        function = self.environment.get(node.name)

        if not isinstance(function, PyraFunction):
            raise RuntimeError(
                f"'{node.name}' is not a function"
            )

        arguments = [
            self.evaluate(argument)
            for argument in node.arguments
        ]

        declaration = function.declaration

        if len(arguments) != len(declaration.parameters):
            raise RuntimeError(
                f"Function '{node.name}' expects "
                f"{len(declaration.parameters)} arguments, "
                f"but received {len(arguments)}"
            )

        previous_environment = self.environment

        function_environment = Environment(
            function.closure
        )

        self.environment = function_environment

        try:

            for parameter, argument in zip(
                declaration.parameters,
                arguments
            ):
                self.environment.define(
                    parameter,
                    argument
                )

            self.execute(declaration.body)

        except ReturnSignal as signal:
            return signal.value

        finally:
            self.environment = previous_environment

        return None

    # =========================
    # TRUTHINESS
    # =========================

    def is_truthy(self, value):

        if value is None:
            return False

        if value is False:
            return False

        if value == 0:
            return False

        if value == "":
            return False

        return True
