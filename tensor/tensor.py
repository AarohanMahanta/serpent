import random

class Tensor:
    
    def __init__(self, data):
        self.data = float(data)
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set()
        self._op = ''

    def __repr__(self):
        return f"Tensor(data={self.data}, grad={self.grad})"
    
    def __add__(self, other):
        out = Tensor(self.data + other.data)
        out._prev = {self, other}
        out._op = 'add'

        def _backward():
            self.grad += out.grad
            other.grad += out.grad

        out._backward = _backward
        return out
    
    def backward(self):
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)

        self.grad = 1.0
        for node in reversed(topo):
            node._backward()

    def __mul__(self, other):
        out = Tensor(self.data * other.data)
        out._prev = {self, other}
        out._op = 'mul'

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = _backward
        return out
    
    def __pow__(self, power):
        out = Tensor(self.data ** power)
        out._prev = {self}
        out._op = 'pow'

        def _backward():
            self.grad += (power * self.data ** (power - 1)) * out.grad

        out._backward = _backward
        return out
    
    def __neg__(self):
        return self * Tensor(-1.0)
    
    def __sub__(self, other):
        return self + (-other)
    
    def __truediv__(self, other):
        return self * other ** -1
    
    def relu(self):
        out = Tensor(max(0, self.data))
        out._prev = {self}
        out._op = 'relu'

        def _backward():
            self.grad += (out.data > 0) * out.grad

        out._backward = _backward
        return out

    
class Neuron:
    def __init__(self, n_inputs):
        self.weights = [Tensor(random.uniform(-1, 1)) for _ in range(n_inputs)]
        self.bias = Tensor(0.0)

    def __call__(self, x):
        weighted_sum = sum((w * x_i for w, x_i in zip(self.weights, x)), self.bias) 
        return weighted_sum.relu()
    
    def parameters(self):
        return self.weights + [self.bias]