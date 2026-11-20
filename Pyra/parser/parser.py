
# PYRA - Abstract Syntax Tree Nodes


# Base Node
class ASTNode:
    pass


# =========================
# VALUE NODES
# =========================

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value


class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value


class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value


# =========================
# VARIABLE NODES
# =========================

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name


class VariableDeclarationNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class AssignmentNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


# =========================
# EXPRESSION NODES
# =========================

class BinaryOperationNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class UnaryOperationNode(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand


class FunctionCallNode(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


# =========================
# STATEMENT NODES
# =========================

class PrintNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression


class ExpressionStatementNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression


class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


# =========================
# FUNCTION NODES
# =========================

class FunctionDeclarationNode(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body


class ReturnNode(ASTNode):
    def __init__(self, value=None):
        self.value = value


# =========================
# PROGRAM NODE
# =========================

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements
