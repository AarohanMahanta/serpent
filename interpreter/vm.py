from ast import arg


class VirtualMachine:
    
    def __init__(self):
        self.stack = []
        self.variables = {}

    def run(self, code):
        instructions = list(code.co_code)
        self.i = 0
        while self.i < len(instructions):
            opcode = instructions[self.i]
            arg = instructions[self.i + 1]
            self.i += 2

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

    def op_COMPARE_OP(self, code, arg):
        import dis
        ops = {
            '<':  lambda a, b: a < b,
            '<=': lambda a, b: a <= b,
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '>':  lambda a, b: a > b,
            '>=': lambda a, b: a >= b,
        }
        right = self.stack.pop()
        left = self.stack.pop()
        op = dis.cmp_op[arg]
        self.stack.append(ops[op](left, right))

    def op_POP_JUMP_IF_FALSE(self, code, arg):
        val = self.stack.pop()
        if not val:
            self.i = arg 

    def op_POP_JUMP_IF_TRUE(self, code, arg):
        val = self.stack.pop()
        if val:
            self.i = arg

    def op_JUMP_FORWARD(self, code, arg):
        self.i += arg     

    def op_JUMP_ABSOLUTE(self, code, arg):
        self.i = arg        

    def op_GET_ITER(self, code, arg):
        obj = self.stack.pop()
        self.stack.append(iter(obj))

         