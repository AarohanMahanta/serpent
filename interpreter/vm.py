class VirtualMachine:
    
    def __init__(self):
        self.stack = []

    def run(self, code):
        instructions = list(code.co_code)
        constants = code.co_consts

        i = 0
        while i < len(instructions):
            opcode = instructions[i]
            i += 1

            if opcode == 100:  # LOAD_CONST
                const_index = instructions[i]
                i += 1
                self.stack.append(constants[const_index])
            elif opcode == 83:  # RETURN_VALUE
                return self.stack.pop()
            else:
                raise NotImplementedError(f"Opcode {opcode} not implemented")