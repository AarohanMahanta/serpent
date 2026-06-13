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

            if opcode == 100:  # LOAD_CONST
                self.stack.append(constants[arg])
            elif opcode == 116:  # LOAD_GLOBAL
                self.stack.append(print)  # For simplicity, we only support the print function
            elif opcode == 1:  # POP_TOP
                self.stack.pop()
            elif opcode == 83:  # RETURN_VALUE
                return self.stack.pop()
            elif opcode == 90:  # BINARY_ADD
            else:
                raise NotImplementedError(f"Opcode {opcode} not implemented")