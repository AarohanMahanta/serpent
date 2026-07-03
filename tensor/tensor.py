import random
import math

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
    
    def tanh(self):
        t = math.tanh(self.data)
        out = Tensor(t)
        out._prev = {self}
        out._op = 'tanh'

        def _backward():
            self.grad += (1 - t**2) * out.grad

        out._backward = _backward
        return out

    
class Neuron:
    def __init__(self, n_inputs):
        self.w = [Tensor(random.uniform(-1, 1)) for _ in range(n_inputs)]
        self.b = Tensor(0.0)

    def __call__(self, x):
        out = sum((wi * xi for wi, xi in zip(self.w, x)), self.b)
        return out.tanh()

    def parameters(self):
        return self.w + [self.b]
    
class Layer:
    def __init__(self, n_inputs, n_neurons):
        self.neurons = [Neuron(n_inputs) for _ in range(n_neurons)]
    
    def __call__(self, x):
        return [neuron(x) for neuron in self.neurons]
    
    def parameters(self):
        return [param for neuron in self.neurons for param in neuron.parameters()]  
    
class MLP:
    def __init__(self, n_inputs, layer_sizes):
        sizes = [n_inputs] + layer_sizes
        self.layers = [Layer(sizes[i], sizes[i+1]) for i in range(len(layer_sizes))]

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x[0] if len(x) == 1 else x
    
    def parameters(self):
        return [param for layer in self.layers for param in layer.parameters()]