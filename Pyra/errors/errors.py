
# PYRA - Error Handling


class PyraError(Exception):

    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column

        location = ""

        if line is not None:
            location = f" at line {line}"

            if column is not None:
                location += f", column {column}"

        super().__init__(f"PYRA Error: {message}{location}")


class PyraSyntaxError(PyraError):
    pass


class PyraRuntimeError(PyraError):
    pass


class PyraNameError(PyraRuntimeError):
    pass


class PyraTypeError(PyraRuntimeError):
    pass


class PyraZeroDivisionError(PyraRuntimeError):
    pass
