from tensor.tensor import Tensor, MLP
import random

random.seed(42)

xs = [
    [Tensor(2.0),  Tensor(3.0),  Tensor(-1.0)],
    [Tensor(3.0),  Tensor(-1.0), Tensor(0.5)],
    [Tensor(0.5),  Tensor(1.0),  Tensor(1.0)],
    [Tensor(1.0),  Tensor(1.0),  Tensor(-1.0)],
]
ys = [Tensor(1.0), Tensor(-1.0), Tensor(-1.0), Tensor(1.0)]

model = MLP(3, [4, 4, 1])

for step in range(50):
    preds = [model(x) for x in xs]

    loss = sum(((p - y) ** 2 for p, y in zip(preds, ys)), Tensor(0.0))

    for p in model.parameters():
        p.grad = 0.0
    loss.backward()

    for p in model.parameters():
        p.data -= 0.05 * p.grad

    if step % 10 == 0:
        print(f"step {step}: loss = {loss.data:.4f}")

print("\nfinal predictions:")
for x, y in zip(xs, ys):
    pred = model(x)
    print(f"  target: {y.data:5.1f}  predicted: {pred.data:.4f}")