class CompilerRuntime:
    def error(self, message):
        raise Exception("Runtime error: " + message)

