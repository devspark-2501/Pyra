
# PYRA - Variable Environment


class Environment:

    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    # Create a variable in the current scope
    def define(self, name, value):

        if name in self.values:
            raise RuntimeError(
                f"Variable '{name}' is already declared"
            )

        self.values[name] = value

    # Get a variable's value
    def get(self, name):

        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise RuntimeError(
            f"Undefined variable '{name}'"
        )

    # Update an existing variable
    def assign(self, name, value):

        if name in self.values:
            self.values[name] = value
            return

        if self.parent is not None:
            self.parent.assign(name, value)
            return

        raise RuntimeError(
            f"Undefined variable '{name}'"
        )

    # Create a child scope
    def create_child(self):
        return Environment(self)
