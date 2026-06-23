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
