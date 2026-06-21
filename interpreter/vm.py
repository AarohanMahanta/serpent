import dis
import builtins


class Frame:
    def __init__(self, code, local_vars=None):
        self.code = code
        self.stack = []
        self.local_vars = local_vars or {}
        self.i = 0
        self.return_value = None


class Function:
    def __init__(self, name, code, vm):
        self.name = name
        self.code = code
        self.vm = vm

    def __call__(self, *args):
        arg_names = self.code.co_varnames[:self.code.co_argcount]
        local_vars = dict(zip(arg_names, args))
        frame = Frame(self.code, local_vars)
        return self.vm.run_frame(frame)


class VirtualMachine:
    def __init__(self):
        self.frames = []
        self.variables = {}

    def run(self, code):
        frame = Frame(code)
        return self.run_frame(frame)

    def run_frame(self, frame):
        self.frames.append(frame)
        instructions = list(frame.code.co_code)

        while frame.i < len(instructions):
            opcode = instructions[frame.i]
            arg = instructions[frame.i + 1]
            frame.i += 2

            opcode_name = dis.opname[opcode]
            method = getattr(self, f"op_{opcode_name}", None)

            if method is None:
                raise NotImplementedError(f"Opcode {opcode_name} not implemented")

            result = method(frame, arg)

            if result == "return":
                self.frames.pop()
                return frame.return_value

        self.frames.pop()

    def op_LOAD_CONST(self, frame, arg):
        frame.stack.append(frame.code.co_consts[arg])

    def op_STORE_NAME(self, frame, arg):
        name = frame.code.co_names[arg]
        self.variables[name] = frame.stack.pop()

    def op_LOAD_NAME(self, frame, arg):
        name = frame.code.co_names[arg]
        if name in frame.local_vars:
            frame.stack.append(frame.local_vars[name])
        elif name in self.variables:
            frame.stack.append(self.variables[name])
        elif hasattr(builtins, name):
            frame.stack.append(getattr(builtins, name))
        else:
            raise NameError(f"name '{name}' is not defined")

    def op_LOAD_FAST(self, frame, arg):
        name = frame.code.co_varnames[arg]
        frame.stack.append(frame.local_vars[name])

    def op_STORE_FAST(self, frame, arg):
        name = frame.code.co_varnames[arg]
        frame.local_vars[name] = frame.stack.pop()

    def op_LOAD_GLOBAL(self, frame, arg):
        name = frame.code.co_names[arg]
        if hasattr(builtins, name):
            frame.stack.append(getattr(builtins, name))
        else:
            raise NameError(f"global name '{name}' is not defined")

    def op_POP_TOP(self, frame, arg):
        frame.stack.pop()

    def op_RETURN_VALUE(self, frame, arg):
        frame.return_value = frame.stack.pop() if frame.stack else None
        return "return"

    def op_CALL_FUNCTION(self, frame, arg):
        args = []
        for _ in range(arg):
            args.insert(0, frame.stack.pop())
        func = frame.stack.pop()
        result = func(*args)
        frame.stack.append(result)

    def op_MAKE_FUNCTION(self, frame, arg):
        name = frame.stack.pop()
        code = frame.stack.pop()
        frame.stack.append(Function(name, code, self))

    def op_BINARY_ADD(self, frame, arg):
        right = frame.stack.pop()
        left = frame.stack.pop()
        frame.stack.append(left + right)

    def op_BINARY_SUBTRACT(self, frame, arg):
        right = frame.stack.pop()
        left = frame.stack.pop()
        frame.stack.append(left - right)

    def op_BINARY_MULTIPLY(self, frame, arg):
        right = frame.stack.pop()
        left = frame.stack.pop()
        frame.stack.append(left * right)

    def op_BINARY_TRUE_DIVIDE(self, frame, arg):
        right = frame.stack.pop()
        left = frame.stack.pop()
        frame.stack.append(left / right)

    def op_BINARY_MODULO(self, frame, arg):
        right = frame.stack.pop()
        left = frame.stack.pop()
        frame.stack.append(left % right)

    def op_BINARY_POWER(self, frame, arg):
        right = frame.stack.pop()
        left = frame.stack.pop()
        frame.stack.append(left ** right)

    def op_COMPARE_OP(self, frame, arg):
        ops = {
            '<':  lambda a, b: a < b,
            '<=': lambda a, b: a <= b,
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '>':  lambda a, b: a > b,
            '>=': lambda a, b: a >= b,
        }
        right = frame.stack.pop()
        left = frame.stack.pop()
        op = dis.cmp_op[arg]
        frame.stack.append(ops[op](left, right))

    def op_POP_JUMP_IF_FALSE(self, frame, arg):
        val = frame.stack.pop()
        if not val:
            frame.i = arg

    def op_POP_JUMP_IF_TRUE(self, frame, arg):
        val = frame.stack.pop()
        if val:
            frame.i = arg

    def op_JUMP_FORWARD(self, frame, arg):
        frame.i += arg

    def op_JUMP_ABSOLUTE(self, frame, arg):
        frame.i = arg

    def op_GET_ITER(self, frame, arg):
        frame.stack.append(iter(frame.stack.pop()))

    def op_FOR_ITER(self, frame, arg):
        iterator = frame.stack[-1]
        try:
            frame.stack.append(next(iterator))
        except StopIteration:
            frame.stack.pop()
            frame.i += arg