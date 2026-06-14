class VirtualMachine:
    
    def __init__(self):
        self.stack = []
        self.variables = {}

    def run(self, code):
        instructions = list(code.co_code)
        constants = code.co_consts

        i = 0
        while i < len(instructions):
            opcode = instructions[i]
            arg = instructions[i + 1]
            i += 2

            # look up method by opcode name instead of elif chain
            import dis
            opcode_name = dis.opname[opcode]
            method = getattr(self, f"op_{opcode_name}", None)

            if method is None:
                raise NotImplementedError(f"Opcode {opcode_name} not implemented")
            
            method(code, arg)

    def op_LOAD_CONST(self, code, arg):
        self.stack.append(code.co_consts[arg])

    def op_STORE_NAME(self, code, arg):
        name = code.co_names[arg]
        self.variables[name] = self.stack.pop()

    def op_LOAD_NAME(self, code, arg):
        import builtins
        name = code.co_names[arg]
        if name in self.variables:
            self.stack.append(self.variables[name])
        elif hasattr(builtins, name):
            self.stack.append(getattr(builtins, name))
        else:
            raise NameError(f"name '{name}' is not defined")

    def op_LOAD_GLOBAL(self, code, arg):
        name = code.co_names[arg]
        # check builtins like print, len etc
        import builtins
        self.stack.append(getattr(builtins, name))

    def op_POP_TOP(self, code, arg):
        self.stack.pop()

    def op_RETURN_VALUE(self, code, arg):
        return self.stack.pop() if self.stack else None

    def op_CALL_FUNCTION(self, code, arg):
        # arg = number of arguments
        args = []
        for _ in range(arg):
            args.insert(0, self.stack.pop())
        func = self.stack.pop()
        result = func(*args)
        self.stack.append(result)

    def op_BINARY_ADD(self, code, arg):
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(left + right)

    def op_BINARY_SUBTRACT(self, code, arg):
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(left - right)

    def op_BINARY_MULTIPLY(self, code, arg):
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(left * right)

    def op_BINARY_TRUE_DIVIDE(self, code, arg):
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(left / right)

    def op_BINARY_MODULO(self, code, arg):
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(left % right)

    def op_BINARY_POWER(self, code, arg):
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(left ** right)