# Serpent

A Python execution engine built from scratch. 
Starting as a bytecode interpreter and growing into a tensor engine, computation graph optimizer, and neural network compiler.

---

## Architecture

```
Layer 1: Bytecode Interpreter    ← complete
Layer 2: Tensor Engine           ← coming soon
Layer 3: Computation Graph       ← coming soon
Layer 4: Graph Optimizer         ← coming soon
Layer 5: C Codegen               ← coming soon
Layer 6: JIT Compilation         ← coming soon
```

---

## Layer 1 — Bytecode Interpreter

A Python bytecode virtual machine written from scratch. Takes any Python script, compiles it to bytecode using CPython's compiler, and executes it through a custom stack-based VM, replicating what CPython does internally.

### How it works

```
script.py (source code)
      ↓
compile()          — CPython turns source into bytecode
      ↓
bytecode           — sequence of opcodes and arguments
      ↓
VirtualMachine     — Serpent executes it instruction by instruction
      ↓
output
```

### What's implemented

- Stack-based virtual machine with a dynamic opcode dispatcher
- Frame system: each function call gets its own isolated stack and local variables
- Variables: local, global, and builtin name lookup
- Math operations: `+`, `-`, `*`, `/`, `%`, `**`
- Comparison operators: `<`, `<=`, `==`, `!=`, `>`, `>=`
- Control flow: `if`, `else`, `elif`
- Loops: `for` loops with iterators
- Functions: `def`, `return`, arguments, recursive calls
- Builtins: `print`, `range`, `iter`, `next`

### Usage

```bash
python3 run.py your_script.py
```

### Example

```python
# hello.py
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

for i in range(10):
    print(fibonacci(i))
```

```bash
python3 run.py hello.py

0
1
1
2
3
5
8
13
21
34
```

### Implementation

The VM uses a dynamic dispatch pattern instead of a giant if/elif chain. Each opcode maps directly to a method:

```python
opcode_name = dis.opname[opcode]          # 100 -> "LOAD_CONST"
method = getattr(self, f"op_{opcode_name}") # finds op_LOAD_CONST
method(frame, arg)                          # executes it
```

Adding a new opcode is just adding a new method. Same architecture used by CPython (`ceval.c`) and the Byterun project.

### File structure

```
serpent/
├── interpreter/
│   └── vm.py       — VirtualMachine, Frame, Function classes
├── tests/
│   └── test_vm.py  — unit tests
└── run.py          — entry point
```

---
