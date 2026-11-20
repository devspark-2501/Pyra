
# PYRA - Runtime Values


class PyraFunction:

    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def __repr__(self):
        return f"<function {self.declaration.name}>"


class ReturnSignal:

    def __init__(self, value):
        self.value = value
