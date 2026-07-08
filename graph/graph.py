class Node:
    def __init__(self, tensor):
        self.id = id(tensor)
        self.op = tensor._op or 'input'
        self.data = round(tensor.data, 4)
        self.grad = round(tensor.grad, 4)

    def __repr__(self):
        return f"Node(op={self.op}, data={self.data}, grad={self.grad})"


class Graph:
    def __init__(self, output):
        self.nodes = {}
        self.edges = []
        self._build(output)

    def _build(self, tensor):
        if id(tensor) in self.nodes:
            return
        self.nodes[id(tensor)] = Node(tensor)
        for child in tensor._prev:
            self._build(child)
            self.edges.append((id(child), id(tensor)))
