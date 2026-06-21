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

A Python bytecode virtual machine written from scratch. Takes any Python script, compiles it to bytecode using CPython's compiler, and executes it through a custom stack-based VM — replicating what CPython does internally.

