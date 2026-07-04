# Serpent - ML Compiler & Runtime
A Python execution engine built from scratch.
Starting as a bytecode interpreter and growing into a tensor engine, computation graph optimizer, and neural network compiler.

---

## Architecture

```
Layer 1: Bytecode Interpreter    ← complete
Layer 2: Tensor Engine           ← complete
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
opcode_name = dis.opname[opcode]            # 100 -> "LOAD_CONST"
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

## Layer 2 — Tensor Engine

A scalar-valued automatic differentiation engine built from scratch. Every operation on a Tensor records how to compute its gradient, so calling `backward()` on any output automatically propagates gradients back through the entire computation — no PyTorch, no NumPy.

### How it works

```
forward pass:   x → [*] → [+] → [tanh] → output
                    records _backward at each step

backward pass:  x ← [*] ← [+] ← [tanh] ← output.grad = 1.0
                    chains _backward functions in reverse
```

### What's implemented

- `Tensor` class with `data` and `grad`
- Operations with automatic gradient tracking: `+`, `-`, `*`, `/`, `**`
- Activation functions: ReLU, tanh
- `backward()` — topological sort of the computation graph, reverse-mode autodiff
- `Neuron`, `Layer`, `MLP` classes for building neural networks
- Training loop with gradient descent

### Example

```python
from tensor.tensor import Tensor, MLP

model = MLP(3, [4, 4, 1])

xs = [
    [Tensor(2.0),  Tensor(3.0),  Tensor(-1.0)],
    [Tensor(3.0),  Tensor(-1.0), Tensor(0.5)],
    [Tensor(0.5),  Tensor(1.0),  Tensor(1.0)],
    [Tensor(1.0),  Tensor(1.0),  Tensor(-1.0)],
]
ys = [Tensor(1.0), Tensor(-1.0), Tensor(-1.0), Tensor(1.0)]

for step in range(50):
    preds = [model(x) for x in xs]
    loss = sum(((p - y) ** 2 for p, y in zip(preds, ys)), Tensor(0.0))
    for p in model.parameters():
        p.grad = 0.0
    loss.backward()
    for p in model.parameters():
        p.data -= 0.05 * p.grad
```

```
step 0:  loss = 5.2788
step 10: loss = 0.3966
step 20: loss = 0.1106
step 30: loss = 0.0577
step 40: loss = 0.0377

final predictions:
  target:   1.0  predicted: 0.9461
  target:  -1.0  predicted: -0.9023
  target:  -1.0  predicted: -0.9274
  target:   1.0  predicted: 0.9014
```

### File structure

```
serpent/
├── tensor/
│   └── tensor.py   — Tensor, Neuron, Layer, MLP classes
└── train.py        — training loop
```

---

## What's next

Layer 3 builds a computation graph on top of the tensor engine, capturing neural network operations as a graph of nodes and edges, which enables the optimizer in Layer 4 to fuse and eliminate operations before codegen.

---

*Built as a ground-up reimplementation of the Python + ML infrastructure stack.*
