class Node:
    def __init__(self, tensor):
        self.id = id(tensor)
        self.op = tensor._op or 'input'
        self.data = round(tensor.data, 4)
        self.grad = round(tensor.grad, 4)

    def __repr__(self):
        return f"Node(op={self.op}, data={self.data}, grad={self.grad})"
